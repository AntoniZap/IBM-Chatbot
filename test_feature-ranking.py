import pymongo
from pymongo import MongoClient
import random
import FeatureRanking

uri = "mongodb+srv://admin:wzE6nBcB4bnpyDUY@ibm.zbskp8h.mongodb.net/?retryWrites=true&w=majority&appName=IBM"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client["IBM"]
collection = db["feature_ranking"]
LLM = ""
def test_addRating1():
        # Test adding a single rating
        User_id = "test_addRating1"
        llm = "OpenAI"
        rating = 4.5
        FeatureRanking.addRating1(User_id, llm, rating)
        print (FeatureRanking.getUserRating(User_id, llm))
        collection.delete_many({"User_id" : "test_addRating1"})

def test_addRating2():
    # Test adding two ratings
    User_id = "test_addRating2"
    llm1 = "OpenAI"
    rating1 = 4.5
    llm2 = "AI21"
    rating2 = 3.0
    FeatureRanking.addRating2(User_id, llm1, rating1, llm2, rating2)
    # Get user ratings
    assert FeatureRanking.getUserRating(User_id, llm1) == rating1
    assert FeatureRanking.getUserRating(User_id, llm2) == rating2
    collection.delete_many({"User_id" : "test_addRating2"})

def test_addRating3():
    # Test adding three ratings
    User_id = "test_addRating3"
    llm1 = "OpenAI"
    rating1 = 4.5
    llm2 = "AI21"
    rating2 = 3.0
    llm3 = "LLAMA"
    rating3 = 2.0
    FeatureRanking.addRating3(User_id, llm1, rating1, llm2, rating2, llm3, rating3)
    # Get user ratings
    assert FeatureRanking.getUserRating(User_id, llm1) == rating1
    assert FeatureRanking.getUserRating(User_id, llm2) == rating2
    assert FeatureRanking.getUserRating(User_id, llm3) == rating3
    collection.delete_many({"User_id" : "test_addRating3"})

    
def test_getAverageRating():
    llm = "getAverageRatingTest"
    User_id1 = "280"
    rating1 = 5
    User_id2 = "233"
    rating2 = 4
    User_id3 = "241"
    rating3 = 3
    FeatureRanking.addRating1(User_id1, llm, rating1)
    FeatureRanking.addRating1(User_id2, llm, rating2)
    FeatureRanking.addRating1(User_id3, llm, rating3)
    assert FeatureRanking.getAverageRating("getAverageRatingTest") == (rating1 + rating2 + rating3) / 3
    collection.delete_many({"LLM" : "getAverageRatingTest"})