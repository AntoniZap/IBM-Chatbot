#UNIT TESTS

#Don't remove these imports
import ChatbotHelper
import config
import os
import ChatbotConcept
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

from normalise import Datafiniti
from local import resolve



def test_get_db():

 # Test 1 - LLM set to not Testing and chroma db exists
 # This will fail if there is no .chroma_db directory
 # Wrong order, first make sure that directory exists, by running a test that would create it first
 # Create instances of ChatbotHelper.get_db()
    db = Chroma(
            persist_directory=".chroma_db",
            embedding_function=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        )
    db1 = ChatbotHelper.get_db()

 # Perform similarity search
    docs = db.similarity_search("Kindle battery")
    docs1 = db1.similarity_search("Kindle battery")

 # Check if the documents have the same length
    assert len(docs) == len(docs1)

 # Check page_content for each document
    for i in range(len(docs)):
        assert docs[i].page_content == docs1[i].page_content





# Test 2 - LLM set to TESTING and creating new embedding
    #not sure what this line is supposed to do
    os.path.dirname("test")
    # if we are creating new embeddings maybe it's worth to make sure previous ones don't exist??? / or they might get overwritten then it's fine
    documents = Datafiniti("Test_Dataset.csv").load()[:1]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
    split_documents = text_splitter.split_documents(documents)
 # Create instances of ChatbotHelper.get_db()
    db = Chroma.from_documents(
            split_documents,
            SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"),
            ids=[str(i) for i in range(len(split_documents))],
            persist_directory=".chroma_db"
        )

    db1 = ChatbotHelper.get_db()
 # Perform similarity search
    docs = db.similarity_search("Kindle battery")
    docs1 = db1.similarity_search("Kindle battery")

 # Check if the documents have the same length
    assert len(docs) == len(docs1)

 # Check page_content for each document
    for i in range(len(docs)):
        assert docs[i].page_content == docs1[i].page_content




# Test 3 - for LLM environ not set to TESTING and create new embeddings
    os.environ['LLM'] = 'AI21'
    documents = Datafiniti("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv").load()[:10] # take the first 10 rows
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
    split_documents = text_splitter.split_documents(documents)
    model = SentenceTransformer("all-MiniLM-L6-v2")

 # Create instances of ChatbotHelper.get_db()
    db = Chroma.from_documents(
            split_documents,
            SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"),
            ids=[str(i) for i in range(len(split_documents))],
            persist_directory=".chroma_db"
        )
    db1 = ChatbotHelper.get_db()

 # Perform similarity search
    docs = db.similarity_search("Kindle battery")
    docs1 = db1.similarity_search("Kindle battery")

 # Check if the documents have the same length
    assert len(docs) == len(docs1)

 # Check page_content for each document
    for i in range(len(docs)):
        assert docs[i].page_content == docs1[i].page_content




# Test 4 - LLM environment not set to Testing and chromedb exists
 # Maybe Explictly set the LLM variable so that it's visible
    os.path.dirname("test") 
    
 # Create instances of ChatbotHelper.get_db()
    db = Chroma(
            persist_directory=".chroma_db",
            embedding_function=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        )
    db1 = ChatbotHelper.get_db()

 # Perform similarity search
    docs = db.similarity_search("Kindle battery")
    docs1 = db1.similarity_search("Kindle battery")

 # Check if the documents have the same length
    assert len(docs) == len(docs1)

 # Check page_content for each document
    for i in range(len(docs)):
        assert docs[i].page_content == docs1[i].page_content  


def test_get_options():
   assert ChatbotHelper.get_options() == {"language" : "English"}

