from database import DatabaseObjectManager


class Writer:
    def __init__(self, db_name, coll_name):
        self.db_manager = DatabaseObjectManager()
        self.db = self.db_manager.getDatabase(db_name)
        self.collection = self.db_manager.getCollection(db_name, coll_name)

    def add_document(self, record):
        """ Add one record to specified collection, returns id of inserted object """
        return self.collection.insert_one(record)

    def add_dataset(self, dataset):
        """ As an input function takes list of objects and return list of their ids """
        return self.collection.insert_many(dataset)
