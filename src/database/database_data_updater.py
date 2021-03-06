from database import DatabaseObjectManager


class DocumentUpdater:
    def __init__(self, db_name, coll_name):
        self.db_manager = DatabaseObjectManager()
        self.db = self.db_manager.get_database(db_name)
        self.collection = self.db_manager.get_collection(db_name, coll_name)

    def query_update(self, query, new_values):
        """ Update all queried records with values from new_values dictionary """
        updated = {"$set": new_values}
        return self.collection.update_many(query, updated)
