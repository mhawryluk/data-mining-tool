import os
import sys
from unittest import TestCase  # if authorization fails, set env variable MONGO_PASS

import pandas as pd

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../../src"))
from src.database import DocumentRemover, Reader, Writer


class TestReader(TestCase):
    def setUp(self) -> None:
        self.reader = Reader("test", "test")
        self.query_test_result = [
            {"key": "value", "another_key": 1},
            {"key": "value", "another_key": 1},
            {"key": "value", "another_key": 1},
            {"key": "value", "another_key": 1},
        ]
        DocumentRemover("test", "test").remove_all()
        writer = Writer("test", "test")
        for i in range(4):
            writer.add_document({"key": "value", "another_key": 1})

    def test_execute_query(self):
        self.assertEqual(
            self.reader.execute_query(columns=["key", "another_key"]),
            self.query_test_result,
        )

    def test_get_nth_chunk(self):
        df = pd.DataFrame(self.query_test_result)
        self.assertDictEqual(df.to_dict(), self.reader.get_nth_chunk().to_dict())

    def test_get_rows_number(self):
        self.assertEqual(self.reader.get_rows_number(), 4)

    def test_get_columns_names(self):
        self.assertEqual(self.reader.get_columns_names(), ["_id", "key", "another_key"])
