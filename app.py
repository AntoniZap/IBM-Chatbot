import os
import os.path
import itertools
import uuid

# Document loading and the link
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain.docstore.document import Document

# ✨AI✨
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.memory import ChatMessageHistory

# Our own stuff
from csv_to_langchain import CSVLoader
from local import resolve
import config

import functools
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Iterator, List, Optional, Union
from dataclasses import dataclass, field
import datetime

@dataclass
class PendingInferenceComplete:
    data: object
    timestamp: str = field(default_factory=lambda: str(datetime.datetime.now()))

@dataclass
class PendingResponseChoice:
    answers: Dict[str, str]
    """
    A mapping from llm names → answers
    """

def get_datafiniti_documents(file_name: str) -> List[Document]:
    loader = CSVLoader(
       file_name,
       metadata_columns=["reviews.rating", "reviews.date"],
       metadata_column_names=["rating", "date"]
    )
    documents = loader.load()
    return documents

@functools.cache
def get_db():
    documents = get_datafiniti_documents("_Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv")
    print("Loading persisted ChromaDB data store")
    db = Chroma(
        persist_directory=".chroma_db",
        embedding_function=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    )
    populate_db(db, documents)
    return db

@dataclass
class PopulateDBResult:
    updated_documents: int
    """
    The number of documents that had to have their metadata updated
    """
    
    new_documents: int
    """
    The number of documents that had to be added.
    """
    
    existing_documents: int
    """
    The number of documents that existed already in the database.
    """

def populate_db(db: Chroma, documents: List[Document]) -> PopulateDBResult:
    persisted_documents = db.get()

    print("Figuring out which documents exist already")
    existing_documents = set((metadata["source"], metadata["row"]) for metadata in persisted_documents["metadatas"])
    document_map = {(document.metadata["source"], document.metadata["row"]) : document for document in documents}
    new_documents = [document_map[key] for key in set(document_map.keys()).difference(existing_documents)]
    
    new_metadata_ids = []
    new_metadata_metadatas = []
    for id, metadata in zip(persisted_documents["ids"], persisted_documents["metadatas"]):
        key = (metadata["source"], metadata["row"])
        try:
            parent_document = document_map[key]
            if parent_document.metadata != metadata:
                new_metadata_ids.append(id)
                new_metadata_metadatas.append(parent_document.metadata)
        except KeyError:
            print(f"document {key} does not has an invalid parent, not considering for metadata update")
            continue

    if len(new_metadata_ids) > 0:
        print(f"Need to update the metadata for {len(new_metadata_ids)} documents")
        if config.FEEDBOT_IGNORE_NEW_DOCUMENTS:
            print("\tFEEDBOT_IGNORE_NEW_DOCUMENTS is set, skipping…")
        else:
            i = 0
            while i < len(new_metadata_ids):
                db._client \
                  .get_collection("langchain") \
                  .update(ids=new_metadata_ids[i:i+5000],
                          metadatas=new_metadata_metadatas[i:i+5000])
                i += 5000
                print(f"Hit {i} document mark…")
    else:
        print(f"No existing document metadata needs to be changed")

    if len(new_documents) > 0:
        print(f"Need to split and add {len(new_documents)} to ChomaDB")
        if config.FEEDBOT_IGNORE_NEW_DOCUMENTS:
            print("\tFEEDBOT_IGNORE_NEW_DOCUMENTS is set, skipping…")
        else:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
            split_documents = text_splitter.split_documents(new_documents)
            print(f"Split {len(new_documents)} documents. Adding to Chromadb…")
            i = 0
            while i < len(split_documents):
                db.add_documents(split_documents[i:i+5000])
                i += 5000
                print(f"Hit {i} document mark…")
            print(f"Added {len(new_documents)} documents to ChromaDB")
    else:
        print(f"All {len(new_documents)} are already in the database")
    return PopulateDBResult(
        updated_documents=len(new_metadata_ids),
        new_documents=len(new_documents),
        existing_documents=len(existing_documents)
    )

def query_chain(retriever):
    return (lambda params: params["messages"][-1].content) | retriever

def setup_llama():
    from langchain_community.llms import LlamaCpp
    from langchain.callbacks.manager import CallbackManager
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
    from llama_cpp.llama_cache import LlamaDiskCache
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    llm = LlamaCpp(
        model_path= os.getenv('LLAMA_MODEL_PATH'),
        # callback_manager = callback_manager,
        verbose = False,
        n_ctx=1024,
    )
    llm.client.set_cache(LlamaDiskCache())
    return llm

def setup_chatgpt():
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(temperature = 0.6)
    return llm

def setup_ai21():
    from langchain_community.llms import AI21
    llm = AI21(temperature=0)
    return llm

def set_state(next_state):
    global state
    state = next_state
    print(f"Transitioned to next state {state}")

def get_state():
    global state
    return state

def get_raw_llm(llm_choice):
    global raw_llms
    llm_choice = llm_choice.lower()
    try:
        llm = raw_llms[llm_choice]
    except KeyError:
        if llm_choice == "llama":
            setup = setup_llama
        elif llm_choice == "ai21":
            setup = setup_ai21
        elif llm_choice == "chatgpt":
            setup = setup_chatgpt
        else:
            raise KeyError()
        llm = setup()
        raw_llms[llm_choice] = llm
    return raw_llms[llm_choice]
    
def get_llm(llm_choice):
    global llms
    llm_choice = llm_choice.lower()
    try:
        llm = llms[llm_choice]
    except KeyError:
        llm = get_raw_llm(llm_choice)
        system_prompt = resolve(options["language"], "system_prompt")
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", f"{system_prompt}\n\\{{context}}\n----------"),
                MessagesPlaceholder(variable_name="messages")
            ]
        )
        document_chain = create_stuff_documents_chain(llm, prompt)
        chain = RunnablePassthrough.assign(answer=document_chain)
        llms[llm_choice] = chain
    return llms[llm_choice]

@dataclass
class Closure:
    llm: str
    def __call__(self, part, whole):
        print(f"got message from `{self.llm}`: {part}")
        socketio.emit("socket", {
            "llm": self.llm,
            "answer": whole.get("answer", "")
        })

def _get_data(messages, llm_choices):
    jobs = []
    pool = ThreadPoolExecutor(4)

    question = messages[-1].content
    context = get_db().as_retriever(k=1).invoke(question)
    context_source = RunnablePassthrough.assign(context=lambda _: context)
    
    for llm_choice in llm_choices:
        chain = context_source | get_llm(llm_choice)
        print(f"Submitting task for `{llm_choice}`")
        job = pool.submit(infer, messages, chain, Closure(llm_choice))
        jobs.append((llm_choice, job))

    answers = []
        
    for llm, job in jobs:
        answer = job.result()
        answers.append({
            "llm": llm,
            "answer": answer["answer"]
        })
    
    return answers, context

def infer(messages, chain, callback):
    print("Starting inference for LLM")
    payload = { "messages": messages }
    full = None
    for item in chain.stream(payload):
        if full is None:
            full = item
        else:
            full += item
        if callback is not None:
            callback(item, full)
    return full

set_state(None)
llms = {}
raw_llms = {}
memory = ChatMessageHistory()
options = { "language" : "English" }

if __name__ == "__main__":
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    from flask_socketio import SocketIO
    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="*")
    CORS(app)

    @app.route('/message', methods=['POST'])
    def get_data():
        global state
        if state is not None:
            return jsonify(
                error="Already running inference",
                state=str(state)
            ), 400
        data = request.json
        llm_choices = data.get('llms') or []
        if len(llm_choices) == 0:
            return jsonify(answers={})
        message = data.get('message')
        set_state(PendingInferenceComplete(data=data))
        memory.add_user_message(message)
        answers, sources = _get_data(memory.messages, llm_choices)
        set_state(PendingResponseChoice(answers={ answer["llm"]: answer["answer"] for answer in answers }))
        return jsonify({ "answers": answers, "sources" : [source.page_content for source in sources] })
    
    
    @app.route('/selectAnswer', methods=['POST'])
    def select_response():
        data = request.json
        global state
        if type(state) is not PendingResponseChoice:
            return jsonify(400)
        chosen_answer = data.get('llm')
        global memory
        memory.add_ai_message(state.answers[chosen_answer.lower()])
        set_state(None)
        return jsonify(200)

    app.run(port=5000)
