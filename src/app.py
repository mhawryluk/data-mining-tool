from database.database_writer import Writer
from database.database_reader import Reader
from database.database_data_updater import DocumentUpdater


def main():
    db = "test1"
    collection = "newcollection"
    query = {"value": {"$gt": 20}}
    writer = Writer(db, collection)
    writer.addDataset([{"code": "qwerty", "value": 12}, {"code": "daad", "value": 13}, {"code": "asdf", "value": 41}, {"code": "aaa", "value": 33}])

    reader = Reader(db, collection)
    print(reader.executeQuery(query, ["code", "value"]))

    updater = DocumentUpdater(db, collection)
    updater.queryUpdate(query, {"code": "updated!"})

    print(reader.executeQuery(query, ["code", "value"]))


if __name__ == '__main__':
    main()
