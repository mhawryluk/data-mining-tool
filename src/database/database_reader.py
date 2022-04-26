from database import DatabaseObjectManager
import pandas as pd


class Reader:
    def __init__(self, db_name, coll_name):
        self.db_manager = DatabaseObjectManager()
        self.db = self.db_manager.get_database(db_name)
        self.collection = self.db_manager.get_collection(db_name, coll_name)

    def execute_query(self, query=None, columns=None, use_id=0, limit=0):
        """ Make a query for specified collection and return result as a list """
        if columns is None:
            columns = self.get_columns_names()
        if query is None:
            query = {}
        fields_selected = {}
        for name in columns:
            fields_selected[name] = 1
        fields_selected['_id'] = use_id
        return list(self.collection.find(query, fields_selected).limit(limit)) # maybe changed to another format

    def get_nth_chunk(self, query=None, columns=None, use_id=0, chunk_size=0, chunk_number=0):
        """ Returns a n-th chunk of data from database, chunks are indexed from 0 """
        if columns is None:
            columns = self.get_columns_names()
        if query is None:
            query = {}
        fields_selected = {}
        for name in columns:
            fields_selected[name] = 1
        fields_selected['_id'] = use_id
        chunk = self.collection.find(query, fields_selected).skip(chunk_size*chunk_number).limit(chunk_size)
        return pd.DataFrame(list(chunk))

    def get_rows_number(self):
        return self.collection.count_documents({})

    def get_columns_names(self):
        return list(self.collection.find_one().keys())
