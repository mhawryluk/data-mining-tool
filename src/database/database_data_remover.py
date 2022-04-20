from .database_manager import DatabaseObjectManager


class DocumentRemover:
    def __init__(self, db_name, coll_name):
        self.db_manager = DatabaseObjectManager()
        self.db = self.db_manager.getDatabase(db_name)
        self.collection = self.db_manager.getCollection(db_name, coll_name)

    def queryRemove(self, query):
        """ Remove all elements that passed the query """
        return self.collection.delete_many(query)

    def removeAll(self):
        """ Clear a collection """
        return self.collection.delete_many({})
