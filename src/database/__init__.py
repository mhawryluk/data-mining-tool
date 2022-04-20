from pymongo import MongoClient

client = MongoClient('mongodb+srv://admin:FvjBbir5bhJl7GvC@dataminingtooldb.trcgm.mongodb.net/')
print(client.list_database_names())
