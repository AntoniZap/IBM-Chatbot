import os
import os.path
import sys
# Document loading and the linke
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
from normalise import Datafiniti
from local import resolve

# streamlit
import streamlit as st



@st.cache_resource()
def get_db():
    import config
    global test_mode
    if config.LLM == "TESTING":
        documents = Datafiniti("Test_Dataset.csv").load()[:1]
    else:
        documents = Datafiniti("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv").load()[:10] # take the first 10 rows
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
def get_llm():
    import config
    if config.LLM == "LLAMA":
        from langchain_community.llms import LlamaCpp
        from langchain.callbacks.manager import CallbackManager
        from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        llm = LlamaCpp(
            model_path=config.LLAMA_MODEL_PATH,
            callback_manager = callback_manager,
            verbose = True,
            n_ctx=1024,
        )
    elif config.LLM == "CHATGPT":
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(temperature = 0.6)
    elif config.LLM == "AI21":
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
import config
db = get_db()
if config.LLM != "TESTING":
    llm = get_llm()
else:
    print("UI test mode, not testing LLM.")
    sys.exit(0)
memory = get_memory()
options = get_options()

language = st.sidebar.selectbox(resolve(options["language"], "select_language"), ("English", "Gaeilge"))
llm_selection = st.sidebar.selectbox(resolve(options["language"], "select_llm"), ("LLaMa", "OpenAI", "Google", "Meta", "IBM"))
question = st.chat_input(resolve(options["language"], "prompt_placeholder"))

if language:
    options["language"] = language

st.title(resolve(options["language"], "title"))

# prompt template
system_prompt = resolve(options["language"], "system_prompt")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt + "\n{context}\n----------"),
        MessagesPlaceholder(variable_name="messages")
    ]
)

retriever = db.as_retriever(k=1)
if config.LLM != "TESTING":
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = RunnablePassthrough \
        .assign(context=query_chain(retriever)) \
        .assign(answer=document_chain)

for message in memory.messages:
    if type(message) is HumanMessage:
        with st.chat_message(resolve(options["language"], "user_role_label")):
            st.markdown(message.content)
    else:
        with st.chat_message(resolve(options["language"], "assistant_role_label")):
            st.markdown(message.content)

if question is None or question == "":
    print("No question. Exiting")
    exit()

memory.add_user_message(question)

# print("QUESTION IS: ", question)
with st.chat_message(resolve(options["language"], "user_role_label")):
    st.markdown(question)

payload = { "messages": memory.messages }
with st.chat_message(resolve(options["language"], "assistant_role_label")):
    element = st.empty()

st.subheader(resolve(options["language"], "sources"))
context = st.empty()

full = None

with st.spinner(resolve(options["language"], "loading")):
    for item in retrieval_chain.stream(payload):
        if full is None:
            full = item
        else:
            full += item
        if "answer" in full:
            element.write(full["answer"])
        if "context" in full:
            context.write([doc.page_content for doc in full["context"]])
        print(item)
    st.write("\n")


if full is not None:
    if type(full) is str:
        memory.add_ai_message(full)
    else:
        memory.add_ai_message(full["answer"])
