from database import DatabaseObjectManager


class Writer:
    def __init__(self, db_name, coll_name):
        self.db_manager = DatabaseObjectManager()
        self.db = self.db_manager.get_database(db_name)
        self.collection = self.db_manager.get_collection(db_name, coll_name)

    def add_document(self, record):
        """ Takes dictionary and adds it to collection, returns id of inserted object """
        return self.collection.insert_one(record)

    def add_dataset(self, dataframe):
        """ Takes dataframe and adds it to collection, returns list of objects ids """
        return self.collection.insert_many(dataframe.to_dict('records'))
