import functools
import os
import os.path
import shutil
import sys

# Document loading and the link
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
from local import resolve
import config

# streamlit
import streamlit as st
from csv_to_langchain import CSVLoader

@functools.cache
def get_db():
    documents = CSVLoader("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv").load()[:10]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
    split_documents = text_splitter.split_documents(documents)
    if os.path.isdir(".chroma_db"):
        shutil.rmtree(".chroma_db")
    print("Creating new embeddings")
    db = Chroma.from_documents(
        split_documents,
        SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"),
        ids=[str(i) for i in range(len(split_documents))],
        persist_directory=".chroma_db"
    )
    return db


@st.cache_resource()
def get_llm():
    if os.getenv('LLM') == "LLAMA":
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
    elif os.getenv('LLM') == "CHATGPT":
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(temperature = 0.6)
    elif os.getenv('LLM') == "AI21":
       from langchain.llms import AI21
       llm = AI21(temperature=0)
    return llm

@st.cache_resource()
def get_memory():
    memory = ChatMessageHistory()
    return memory

@st.cache_resource()
def get_options():
    return { "language" : "English" }

def query_chain(retriever):
    return (lambda params: params["messages"][-1].content) | retriever

def setup_llama():
    from langchain_community.llms import LlamaCpp
    from langchain.callbacks.manager import CallbackManager
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
    from llama_cpp import LlamaCache
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    llm = LlamaCpp(
        model_path=os.getenv('LLAMA_MODEL_PATH'),
        callback_manager=callback_manager,
        verbose=True,
        n_ctx=1024,
    )
    llm.client.set_cache(LlamaCache())
    return llm

def setup_chatgpt():
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(temperature=0.6)
    return llm

def setup_ai21():
    from langchain_community.llms import AI21
    llm = AI21(temperature=0)
    return llm


@st.cache_resource()
def get_db_legacy():
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

