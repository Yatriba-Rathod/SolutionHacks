from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load your .env file
load_dotenv()

# Get your Mongo URI
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["job_readiness"]  # database name
jobs_col = db["jobs"]         # collection name

# Get all jobs as a list of dictionaries
def get_jobs():
    return list(jobs_col.find({}, {"_id": 0}))  # Exclude _id field

# Get a single job by title
def get_job_by_title(title):
    return jobs_col.find_one({"title": title}, {"_id": 0})

def insert_jobs(jobs):
    if isinstance(jobs, list):
        jobs_col.insert_many(jobs)
    elif isinstance(jobs, dict):
        jobs_col.insert_one(jobs)
    else:
        print("❌ Invalid format. Provide list or dict.")
