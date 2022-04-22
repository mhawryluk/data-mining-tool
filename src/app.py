from database import Writer, Reader, DocumentUpdater


def main():
    db = "test1"
    collection = "newcollection"
    query = {"value": {"$gt": 20}}
    writer = Writer(db, collection)
    writer.add_dataset([{"code": "qwerty", "value": 12}, {"code": "daad", "value": 13}, {"code": "asdf", "value": 41},
                        {"code": "aaa", "value": 33}])

    reader = Reader(db, collection)
    print(reader.execute_query(query, ["code", "value"]))

    updater = DocumentUpdater(db, collection)
    updater.query_update(query, {"code": "updated!"})

    print(reader.execute_query(query, ["code", "value"]))


if __name__ == '__main__':
    main()
