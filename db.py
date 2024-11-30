from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

MONGO_URI = os.getenv("MONGODB_URI", "mongodb+srv://maihar:maihar@cluster0.pad3t.mongodb.net/?retryWrites=true&w=majority&appName=task")

if not MONGO_URI:
    logging.error("MONGODB_URI environment variable is not set.")
else:
    logging.info(f"Connecting to MongoDB with URI: {MONGO_URI}")

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    # Check if the connection is successful by pinging the database
    client.admin.command('ping')
    logging.info("Connected to MongoDB successfully.")
except Exception as e:
    logging.error(f"Failed to connect to MongoDB: {e}")

db = client["student_management"]
students_collection = db["students"]
