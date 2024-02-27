import os
import os.path

# Document loading and the linke
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough

# ✨AI✨
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ChatMessageHistory

# Our own stuff
from csv_to_langchain import CSVLoader
from local import resolve
import config

import functools
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Iterator, List, Optional, Union
from dataclasses import dataclass, field
from queue import Queue

@dataclass
class PendingInferenceComplete:
    pass

@dataclass
class PendingResponseChoice:
    answers: Dict[str, str]
    """
    A mapping from llm names → answers
    """

@functools.cache
def get_db():
    documents = CSVLoader("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv").load()[:10]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
    split_documents = text_splitter.split_documents(documents)
    if os.path.isdir(".chroma_db"):
        print("Loading chromadb from filesystem")
        db = Chroma(
            persist_directory=".chroma_db",
            embedding_function=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        )
    else:
        print("Creating new embeddings")
        db = Chroma.from_documents(
            split_documents,
            SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"),
            ids=[str(i) for i in range(len(split_documents))],
            persist_directory=".chroma_db"
        )
    return db

def query_chain(retriever):
    return (lambda params: params["messages"][-1].content) | retriever

def setup_llama():
    from langchain_community.llms import LlamaCpp
    from langchain.callbacks.manager import CallbackManager
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
    from llama_cpp import LlamaCache
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    llm = LlamaCpp(
        model_path= os.getenv('LLAMA_MODEL_PATH'),
        callback_manager = callback_manager,
        verbose = True,
        n_ctx=1024,
    )
    llm.client.set_cache(LlamaCache())
    return llm

def setup_chatgpt():
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(temperature = 0.6)
    return llm

def setup_ai21():
    from langchain.llms import AI21
    llm = AI21(temperature=0)
    return llm

def set_llm(llm_choice):
    global llm
    llm = llm_choice

def get_llm(llm_choice):
    global llms
    llm_choice = llm_choice.lower()
    try:
        llm = llms[llm_choice]
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
        system_prompt = resolve(options["language"], "system_prompt")
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", f"{system_prompt}\n\\{{context}}\n----------"),
                MessagesPlaceholder(variable_name="messages")
            ]
        )
        retriever = get_db().as_retriever(k=1)
        document_chain = create_stuff_documents_chain(llm, prompt)
        chain = RunnablePassthrough \
            .assign(context=query_chain(retriever)) \
            .assign(answer=document_chain)
        llms[llm_choice] = chain
    return llms[llm_choice]

# Flask
state = None
llms = {}
queue = Queue()
memory = ChatMessageHistory()
options = { "language" : "English" }

llm = config.LLM or 'ChatGPT'
get_llm(config.LLM)

def _get_data(messages, llm_choices):
    jobs = []
    pool = ThreadPoolExecutor(2)
    global socketio
    for llm_choice in llm_choices:
        @dataclass
        class Closure:
            llm: str
            def __call__(self, part, whole):
                print(f"got message from `{self.llm}`: {part}")
                socketio.emit("socket", {
                    "llm": self.llm,
                    "answer": whole.get("answer", "")
                })
                
        chain = get_llm(llm_choice)
        print(f"Submitting task for `{llm_choice}`")
        job = pool.submit(
            infer,
            messages,
            chain,
            Closure(llm_choice)
            # None
        )
        jobs.append((llm_choice, job))

    answers = []
    # sources = [doc.page_content for doc in full[0]["context"]]
        
    for llm, job in jobs:
        answer = job.result()
        answers.append({
            "llm": llm,
            "answer": answer["answer"]
        })
    
    return answers

def infer(messages, chain, cb):
    print("Starting inference for LLM")
    payload = { "messages": messages }
    full = None
    for item in chain.stream(payload):
        if full is None:
            full = item
        else:
            full += item
        if cb is not None:
            cb(item, full)
    return full

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
        return jsonify(error="Already running inference"), 400
    state = PendingInferenceComplete
    data = request.json
    message = data.get('message')
    global llm
    llm_choices = data.get('llms') or [llm]
    global conversation
    memory.add_user_message(message)
    answers = _get_data(memory.messages, llm_choices)
    state = PendingResponseChoice(answers={ answer["llm"]: answer["answer"] for answer in answers })
    return jsonify(answers)

@app.route('/selectAnswer', methods=['POST'])
def select_response():
    data = request.json
    global state
    if type(state) is not PendingResponseChoice:
        return jsonify(400)
    chosen_answer = data.get('llm')
    global memory
    memory.add_ai_message(state.answers[chosen_answer.lower()])
    state = None
    return jsonify(200)

@app.route('/llm', methods=['POST'])
def _get_llm():
    llm_choice = request.json.get('llm')
    set_llm(llm_choice)
    return jsonify(200)

if __name__ == "__main__":
    app.run(port=5000)
