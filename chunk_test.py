import time
from csv_to_langchain import *
from memory_profiler import profile
small_chunk=50
large_chunk=500
PRINT_ACCESSED_DATA=True


def load_documents_original():
    dataholder=[]
    documents_original = CSVLoader("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv").load()
    for i, document in enumerate(documents_original):
        dataholder+=document.page_content.split("\n")
    return(dataholder)
            

def load_n_lines_original(lines_read):
    dataholder=[]
    documents_original = CSVLoader("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv").load()

    for i, document in enumerate(documents_original):
        dataholder+= document.page_content.split("\n")[:lines_read]
        if i==24:
            break
    return(dataholder)


def load_small_documents_chunked():
    dataholder=[]
    chunk_size = small_chunk
    documents_chunked = ChunkedCSVLoader("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv", chunk_size)

    for i, chunk in enumerate(documents_chunked.load_chunks()):
        if chunk:
            for document in chunk:
                dataholder += document.page_content.split("\n")
    return(dataholder)


def load_n_lines_small_chunk(lines_read, chunk_read):
    dataholder=[]
    chunk_size=small_chunk
    documents_chunked = ChunkedCSVLoader("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv", chunk_size)

    start_chunk_index = chunk_read

    for i, chunk in enumerate(documents_chunked.load_chunks(start_chunk_index)):
        if i == 0:
            for j, document in enumerate(chunk[:lines_read]):
                dataholder+=("Line" ,(j+1),"of Chunk",(i+start_chunk_index+1)," ----- ",document.page_content.strip()," ----- ","Reviews Rating:" ,(document.metadata.get('reviews.rating', 'N/A')),"\n\n")
            break
    return(dataholder)


def load_large_documents_chunked():
    dataholder=[]
    chunk_size = small_chunk
    documents_chunked = ChunkedCSVLoader("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv", chunk_size)

    for i, chunk in enumerate(documents_chunked.load_chunks()):
        if chunk:
            for document in chunk:
                dataholder += document.page_content.split("\n")
    return(dataholder)

def load_n_lines_large_chunk(lines_read, chunk_read):
    dataholder=[]
    chunk_size=small_chunk
    documents_chunked = ChunkedCSVLoader("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv", chunk_size)

    start_chunk_index = chunk_read

    for i, chunk in enumerate(documents_chunked.load_chunks(start_chunk_index)):
        if i == 0:
            for j, document in enumerate(chunk[:lines_read]):
                dataholder+=("Line" ,(j+1),"of Chunk",(i+start_chunk_index+1)," ----- ",document.page_content.strip()," ----- ","Reviews Rating:" ,(document.metadata.get('reviews.rating', 'N/A')),"\n\n")
            break
    return(dataholder)

original_All_Start_Time = time.time()
load_documents_original()
original_All_End_Time = time.time()
print("Loading all with original design takes", round(original_All_End_Time - original_All_Start_Time,3), "seconds",end="\n\n")


original_Some_Start_Time = time.time()
load_n_lines_original(lines_read=25)
original_Some_End_Time = time.time()
print("Loading 25 with original design takes", round(original_Some_End_Time - original_Some_Start_Time,3), "seconds",end="\n\n\n")


small_All_Start_Time = time.time()
load_small_documents_chunked()
small_All_End_Time = time.time()
print("loading all small chunks takes", round(small_All_End_Time - small_All_Start_Time,3), "seconds",round((100*(small_All_End_Time - small_All_Start_Time)/(original_All_End_Time - original_All_Start_Time)),3),"% of the original time",end="\n\n\n")

small_Some_Start_Time = time.time()
load_n_lines_small_chunk(lines_read=25, chunk_read=80)
small_Some_End_Time = time.time()
print("loading 25 small chunk lines takes", round(small_Some_End_Time - small_Some_Start_Time,3), "seconds",round((100*(small_Some_End_Time - small_Some_Start_Time)/(original_Some_End_Time - original_Some_Start_Time)),3),"% of the original time",end="\n\n\n")


large_All_Start_Time = time.time()
load_large_documents_chunked()
large_All_End_Time = time.time()
print("loading all large chunks takes", round(large_All_End_Time - large_All_Start_Time,3), "seconds",round((100*(large_All_End_Time - large_All_Start_Time)/(original_All_End_Time - original_All_Start_Time)),3),"% of the original time",end="\n\n\n")


large_Some_Start_Time = time.time()
load_n_lines_large_chunk(lines_read=25, chunk_read=80)
large_Some_End_Time = time.time()
print("loading 25 large chunk lines takes", round(large_Some_End_Time - large_Some_Start_Time,3), "seconds",round((100*(large_Some_End_Time - large_Some_Start_Time)/(original_Some_End_Time - original_Some_Start_Time)),3),"% of the original time",end="\n\n\n")









