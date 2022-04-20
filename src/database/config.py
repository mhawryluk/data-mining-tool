from pymongo import MongoClient
import os

client = MongoClient('mongodb+srv://admin:{}@dataminingtooldb.trcgm.mongodb.net/'.format(os.environ.get("MONGO_PASS")))
