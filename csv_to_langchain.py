import os
import os.path

# Document loading and the linke
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_core.documents.base import Document
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough

# Our own stuff
from normalise import Datafiniti
from local import resolve

class csv_to_langchain:
    loader = CSVLoader(file_path='Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv', source_column='reviews.text', encoding='8859')

    data = loader.load()

    print(data)