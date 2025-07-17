from pymongo import MongoClient
import os

# Connect to MongoDB
MONGO_URI =   # e.g., "mongodb+srv://username:password@cluster0.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(os.getenv("MONGO_URI"))

# Use the 'personaforge_db' database
db = client["personaforge_db"]

# Collection to store users (for login/signup and XP tracking)
users_collection = db["users"]

# Collection to store job listings (for job finder feature)
jobs_collection = db["jobs"]
