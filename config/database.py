#databse connection

from pymongo import MongoClient

def get_database():
    client = MongoClient("mongodb://localhost:27017/users")
    db = client["user_profiles"]
    return db

