from database import DatabaseObjectManager


class Reader:
    def __init__(self, db_name, coll_name):
        self.db_manager = DatabaseObjectManager()
        self.db = self.db_manager.get_database(db_name)
        self.collection = self.db_manager.get_collection(db_name, coll_name)

    def execute_query(self, query, columns, use_id=0, limit=0):
        """ Make a query for specified collection and return result as a list """
        fields_selected = {}
        for name in columns:
            fields_selected[name] = 1
        fields_selected['_id'] = use_id
        return list(self.collection.find(query, fields_selected).limit(limit)) # maybe changed to another format
