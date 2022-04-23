from database import DatabaseObjectManager


class DocumentRemover:
    def __init__(self, db_name, coll_name):
        self.db_manager = DatabaseObjectManager()
        self.db = self.db_manager.get_database(db_name)
        self.collection = self.db_manager.get_collection(db_name, coll_name)

    def query_remove(self, query):
        """ Remove all elements that passed the query """
        return self.collection.delete_many(query)

    def remove_all(self):
        """ Clear a collection """
        return self.collection.delete_many({})
