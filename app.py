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
# if os.getenv('LLM') != "TESTING":
llm = get_llm()
# else:
#     print("UI test mode, not testing LLM.")
#     sys.exit(0)
memory = get_memory()
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
# if os.getenv('LLM') != "TESTING":
document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = RunnablePassthrough \
    .assign(context=query_chain(retriever)) \
    .assign(answer=document_chain)

# for message in memory.messages:
#     if type(message) is HumanMessage:
#         with st.chat_message(resolve(options["language"], "user_role_label")):
            
#     else:
#         with st.chat_message(resolve(options["language"], "assistant_role_label")):
            



# print("QUESTION IS: ", question)

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


# def send_response(answer):
#     print(answer)
    
    

if __name__ == "__main__":
    app.run(port=5000)