from typing import Annotated
from fastapi import Depends
from pymongo import MongoClient
# import os
# from dotenv import load_dotenv
# load_dotenv()
# MONGO_URI = os.getenv("MONGO_URI")
# MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_URI = "mongodb+srv://root:ramibenmrad4@cluster0.b3adovy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_DB_NAME = "testing"
client = MongoClient(MONGO_URI)
db = client.get_database(MONGO_DB_NAME)
async def get_db():
    return db
DB = Annotated[type(db), Depends(get_db)]