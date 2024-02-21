import os
import os.path
import sys

# Document loading and the linke
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

from ChatbotHelper import get_db, get_llm, get_memory, get_options, query_chain
# Our own stuff
from normalise import Datafiniti
from local import resolve
import config

# streamlit
import streamlit as st

# Flask
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
db = get_db()

def setup_env_var():
    setup(os.getenv('LLM'))
    
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