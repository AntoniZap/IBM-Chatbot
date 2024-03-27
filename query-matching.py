# import fuzzy logic library
from thefuzz import process, fuzz
import pymongo
from pymongo import MongoClient
import random

uri = "mongodb+srv://admin:wzE6nBcB4bnpyDUY@ibm.zbskp8h.mongodb.net/?retryWrites=true&w=majority&appName=IBM"
# Connect to the server
client = MongoClient(uri)
db = client["IBM"]
collection = db["feature_ranking"]

#
# Gets all the past queries from the database
#
def get_old_queries():
    entries = collection.find({}, {'Query': 1})
    old_queries = []
    for entry in entries:
        old_queries.append(entry['Query'])
    return old_queries

#
# Returns the LLMs best-ranked for the paramater query
#
def get_best_LLM(query):
    old_queries = get_old_queries()
    matches = process.extract(query, old_queries, score_cutoff = 65, scorer=fuzz.token_set_ratio)
    for match in matches:
        entries_matched = collection.find({"Query" : match})        # Get all rankings for the query 
        positive_ratings = []
        negative_ratings = 0
        no_rating = []
        for entry in entries_matched:
            rating = entry['Rating']
            if rating == 3:
                no_rating.append(entry['LLM'])
            else:
                if rating >= 4:
                    positive_ratings.append({'LLM': entry['LLM'], 'Rating': rating})
                else:
                    negative_ratings +=1
        if positive_ratings:
            max_rating = max(positive_ratings, key=lambda x: x['Rating'])
            best_LLMs = []
            for llm in positive_ratings:
                if llm['Rating'] == max_rating['Rating']:
                    best_LLMs.append(llm['LLM'])
            return best_LLMs
        if negative_ratings > 0 and no_rating:
            return no_rating
        
    return None                                                 # if no ratings were found for any of the matches
            
                

        
    
    
    
    
    
    
    
    
    

