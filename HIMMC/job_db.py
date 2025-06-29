from pymongo import MongoClient
import os

# MongoDB Setup
client = os.getenv("MONGO_URI")
db = client["himyc_database"]
users_collection = db["users"]
jobs_collection = db["jobs"]

def save_jobs_to_db(jobs, role, location):
    for job in jobs:
        job["role_query"] = role
        job["location"] = location
        existing = jobs_collection.find_one({"url": job["url"]})
        if not existing:
            jobs_collection.insert_one(job)
    
def filter_jobs(role, location, filters):
    query = {
        "role_query": {"$regex": role, "$options": "i"},
        "location": {"$regex": location, "$options": "i"}
    }

    if "adhd" in filters:
        query["disabilities"] = {"$in": ["ADHD"]}
    if "physical" in filters:
        query["disabilities"] = {"$in": ["physical disability"]}
    if "no_degree" in filters:
        query["degree_required"] = False

    return list(jobs_collection.find(query))
