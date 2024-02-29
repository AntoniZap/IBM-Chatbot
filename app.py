import os
import os.path
import sys

# Document loading and the link
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_core.documents.base import Document
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough

# ✨AI✨
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.memory import ChatMessageHistory
from langchain.chains.combine_documents import create_stuff_documents_chain

# Our own stuff
from csv_to_langchain import CSVLoader
from local import resolve

# streamlit
import streamlit as st

@st.cache_resource()
def get_db():
    documents = CSVLoader("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv").load()[:10]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
    split_documents = text_splitter.split_documents(documents)
    model = SentenceTransformer("all-MiniLM-L6-v2")
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

@st.cache_resource()
def get_memory():
    global memory
    memory = ChatMessageHistory()
    return memory

@st.cache_resource()
def get_options():
    global options
    options = { "language" : "English" }
    return options

def query_chain(retriever):
    return (lambda params: params["messages"][-1].content) | retriever


# Flask
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


def setup_env_var():
    setup_env = str(os.getenv('LLM'))
    if setup_env == 'None':
        setup("ChatGPT")
    else:
        setup(setup_env)


def setup(llm_choice):
    global llm
    if llm_choice == "LLAMA":
        from langchain_community.llms import LlamaCpp
        from langchain.callbacks.manager import CallbackManager
        from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        
        llm = LlamaCpp(
            model_path= os.getenv('LLAMA_MODEL_PATH'),
            callback_manager = callback_manager,
            verbose = True,
            n_ctx=1024,
        )
    elif llm_choice == "ChatGPT":
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(temperature = 0.6)
    elif llm_choice == "AI21":
       from langchain.llms import AI21
       llm = AI21(temperature=0)
    global memory
    memory = get_memory()
    global options
    options = get_options()

    # prompt template
    system_prompt = resolve(options["language"], "system_prompt")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt + "\n{context}\n----------"),
            MessagesPlaceholder(variable_name="messages")
        ]
    )
    global db
    db = get_db()
    retriever = db.as_retriever(k=1)
    global retrieval_chain
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = RunnablePassthrough \
        .assign(context=query_chain(retriever)) \
        .assign(answer=document_chain)
    
    return llm           

setup_env_var()

@app.route('/message', methods=['POST'])
def get_data():
    data = request.json
    message=data.get('message')
    print(message)
    memory.add_user_message(message)
    payload = { "messages": memory.messages }
    
    full = None

    with st.spinner(resolve(options["language"], "loading")):
        for item in retrieval_chain.stream(payload):
            if full is None:
                full = item
            else:
                full += item
            
            print(item)
        st.write("\n")

    if full is not None:
        if type(full) is str:
            memory.add_ai_message(full)
        else:
            memory.add_ai_message(full["answer"])
    return jsonify(full["answer"])
    
@app.route('/llm', methods=['POST'])
def get_llm():
    data = request.json
    llm_choice=data.get('llm')
    setup(llm_choice)
    return jsonify(200)
    
if __name__ == "__main__":
    app.run(port=5000)