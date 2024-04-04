from thefuzz import process, fuzz
import pymongo
from pymongo import MongoClient
import random
import feature_ranking
import query_matching
from query_matching import get_best_LLM

uri = "mongodb+srv://admin:wzE6nBcB4bnpyDUY@ibm.zbskp8h.mongodb.net/?retryWrites=true&w=majority&appName=IBM"
# Connect to the server
client = MongoClient(uri)
db = client["IBM"]
collection = db["feature_ranking"]



def test_get_best_LLM():
    User_id = "get_best_LLM"
    query1 = "What is the best kindle?"
    llm1 = "OpenAI"
    llm2 = "AI21"
    llm3 = "LLAMA"
    query2 = "What kindle is the best?"

    feature_ranking.addRating3(User_id, query2, llm1, 5.0, llm2, 4.0, llm3, 2.0)
    feature_ranking.addRating3(User_id, query1, llm1, 0.0, llm2, 0.0, llm3, 0.0)

    assert query_matching.get_best_LLM("What is the best kindle?") == ["OpenAI"] # Test for multiple positive ratings
    #assert query_matching.get_best_LLM("Is the battery life good on the kindles, which is best?") == None  # Test for no positive ratings
   # assert query_matching.get_best_LLM("What is the weather like today") == None # Test for no similar queries
    collection.delete_many({"User_id": "get_best_LLM"})
