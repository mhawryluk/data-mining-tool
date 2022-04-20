from .config import client


class DatabaseObjectManager:
    def __init__(self):
        self.db_client = client

    def getDatabase(self, db_name):
        """ Get database by provided name or create new one if it not exists """
        return self.db_client[db_name]

    def getDatabasesList(self):
        """ Get list of all databases """
        return self.db_client.list_database_names()

    def findDatabase(self, db_name):
        """ Check if database with this name is in system """
        db_list = self.db_client.list_database_names()
        return True if db_name in db_list else False

    def getCollection(self, db_name, collection_name):
        """ Get collection by provided name from specified database or create new one if it not exists """
        return self.db_client[db_name][collection_name]

    def getCollectionsList(self, db_name):
        """ Get list of all collections in the database """
        return self.db_client[db_name].list_collection_names()

    def findCollection(self, db_name, coll_name):
        """ Check if collection with this name is in the database """
        db = self.db_client[db_name]
        coll_list = db.list_collection_names()
        return True if coll_name in coll_list else False
