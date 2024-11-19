import unittest
from datetime import datetime
from src.parsers.data_parser import DateParser


class TestDateParser(unittest.TestCase):
    def setUp(self):
        self.date_parser = DateParser()

    def test_parse_valid_date_full_month(self):
        date_str = "19/November/2023:15:30:45 +0000"
        expected_date = datetime(2023, 11, 19, 15, 30, 45, tzinfo=datetime.strptime(date_str, "%d/%B/%Y:%H:%M:%S %z").tzinfo)
        result = self.date_parser.parse(date_str)
        self.assertEqual(result, expected_date)

    def test_parse_valid_date_abbreviated_month(self):
        date_str = "19/Nov/2023:15:30:45 +0000"
        expected_date = datetime(2023, 11, 19, 15, 30, 45, tzinfo=datetime.strptime(date_str, "%d/%b/%Y:%H:%M:%S %z").tzinfo)
        result = self.date_parser.parse(date_str)
        self.assertEqual(result, expected_date)

    def test_parse_invalid_date(self):
        date_str = "Invalid Date String"
        result = self.date_parser.parse(date_str)
        self.assertIsNone(result)

    def test_parse_empty_date(self):
        date_str = ""
        result = self.date_parser.parse(date_str)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
