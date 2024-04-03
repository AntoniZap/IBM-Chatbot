import pymongo
from pymongo import MongoClient
import random

uri = "mongodb+srv://admin:wzE6nBcB4bnpyDUY@ibm.zbskp8h.mongodb.net/?retryWrites=true&w=majority&appName=IBM"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client["IBM"]
collection = db["feature_ranking"]

def addRating1(User_id, querey, llm, rating):
    post = {"User_id" : User_id, "Query": query, "LLM": llm, "Rating" : rating}
    collection.insert_one(post)
    return


def addRating2(User_id, query, llm1, rating1, llm2, rating2):
    post1 = {"User_id": User_id, "Query": query, "LLM": llm1, "Rating": rating1}
    post2 = {"User_id": User_id, "Query": query, "LLM": llm2, "Rating": rating2}
    collection.insert_one(post1)
    _id +=1
    collection.insert_one(post2)
    return


def addRating3(User_id, query, llm1, rating1, llm2, rating2, llm3, rating3):
    post1 = {"User_id": User_id, "Query": query, "LLM": llm1, "Rating": rating1}
    collection.insert_one(post1)
    post2 = {"User_id": User_id, "Query": query, "LLM": llm2, "Rating": rating2}
    collection.insert_one(post2)
    post3 = {"User_id": User_id, "Query": query, "LLM": llm3, "Rating": rating3}
    collection.insert_one(post3)
    return


def getAverageRating(LLM):
    results = collection.find({"LLM": LLM})
    temp = 0
    count = 0
    for result in results:
        count = count + 1
        temp = temp + result["Rating"]

    return temp / count


def getUserRating(User_id, llm):
    result = collection.find_one({"User_id": User_id, "LLM": llm})
    if result is None:
        return None
    return result["Rating"]
