import os
import os.path
import shutil

# Document loading and the link
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough

# ✨AI✨
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ChatMessageHistory

from ChatbotHelper import get_db, query_chain, setup_llama, setup_ai21, setup_chatgpt
# Our own stuff
from csv_to_langchain import CSVLoader
from local import resolve
import config

import functools
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Iterator, List, Optional, Union
from dataclasses import dataclass, field
import time
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
        retriever = get_db().as_retriever(k=1)
        document_chain = create_stuff_documents_chain(llm, prompt)
        chain = RunnablePassthrough \
            .assign(context=query_chain(retriever)) \
            .assign(answer=document_chain)
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
    for llm_choice in llm_choices:
        chain = get_llm(llm_choice)
        print(f"Submitting task for `{llm_choice}`")
        job = pool.submit(infer, messages, chain, Closure(llm_choice))
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


def infer(messages, chain, callback):
    print("Starting inference for LLM")
    payload = {"messages": messages}
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
options = {"language": "English"}

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
        answers = _get_data(memory.messages, llm_choices)
        set_state(PendingResponseChoice(answers={answer["llm"]: answer["answer"] for answer in answers}))
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
        set_state(None)
        return jsonify(200)


    app.run(port=5000)
