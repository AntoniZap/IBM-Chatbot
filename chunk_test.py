import time
from csv_to_langchain import *

input_csv = "Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv"
chunk_size=500
chunk_number=10

start=time.time()
documents_chunked = ChunkedCSVLoader(input_csv, chunk_size)
documents_chunked.seperate_chunks(chunk_size=chunk_size)
chunk=documents_chunked.get_chunk(chunkNumber=chunk_number)
print(time.time()-start,"to chunk the document into:",documents_chunked.get_chunk_amount(), "chunks")


start=time.time()
documents = CSVLoader(input_csv).load()
pseudoChunk=documents[chunk_number*chunk_size:chunk_number*(chunk_size+1)]
print(time.time()-start,"to retrieve the files regularly")


start=time.time()
output_folder = "output_chunks"
split_into_csv(input_csv, output_folder, chunk_size)
print(time.time()-start,"to split all chunks to csv files")
start=time.time()