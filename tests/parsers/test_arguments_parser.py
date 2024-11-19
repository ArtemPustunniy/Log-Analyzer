import unittest
from datetime import datetime
from src.parsers.arguments_parser import ArgumentsParser, DateParser


class TestDateParser(unittest.TestCase):
    def test_parse_valid_date(self):
        result = DateParser.parse("2023-11-19")
        self.assertEqual(result, datetime(2023, 11, 19))

    def test_parse_invalid_date(self):
        result = DateParser.parse("2023-13-40")  # Invalid date
        self.assertIsNone(result)

    def test_check_time_pattern_valid(self):
        result_full = DateParser.check_time_pattern("19/November/2023:15:30:45 +0000")
        self.assertEqual(result_full, datetime(2023, 11, 19, 15, 30, 45, tzinfo=result_full.tzinfo))

        result_abbr = DateParser.check_time_pattern("19/Nov/2023:15:30:45 +0000")
        self.assertEqual(result_abbr, datetime(2023, 11, 19, 15, 30, 45, tzinfo=result_abbr.tzinfo))

    def test_check_time_pattern_invalid(self):
        with self.assertRaises(ValueError):
            DateParser.check_time_pattern("Invalid Date Format")


class TestArgumentsParser(unittest.TestCase):
    def setUp(self):
        self.parser = ArgumentsParser()

    def test_parse_valid_arguments(self):
        args = ["--path", "log1.txt", "--from", "2023-11-01", "--to", "2023-11-19"]
        result = self.parser.parse(args)
        expected = {
            "path": ["log1.txt"],
            "from": "2023-11-01",
            "to": "2023-11-19"
        }
        self.assertEqual(result, expected)

    def test_parse_missing_path(self):
        args = ["--from", "2023-11-01", "--to", "2023-11-19"]
        result = self.parser.parse(args)
        self.assertEqual(result, "Error: --path option is required.")

    def test_parse_invalid_from_date(self):
        args = ["--path", "log1.txt", "--from", "invalid-date", "--to", "2023-11-19"]
        result = self.parser.parse(args)
        self.assertEqual(
            result,
            "Error: Invalid date format for --from option. Expected format is yyyy-MM-dd."
        )

    def test_parse_invalid_to_date(self):
        args = ["--path", "log1.txt", "--from", "2023-11-01", "--to", "invalid-date"]
        result = self.parser.parse(args)
        self.assertEqual(
            result,
            "Error: Invalid date format for --to option. Expected format is yyyy-MM-dd."
        )

    def test_parse_valid_multiple_paths(self):
        args = ["--path", "log1.txt", "--path", "log2.txt", "--from", "2023-11-01"]
        result = self.parser.parse(args)
        expected = {
            "path": ["log1.txt", "log2.txt"],
            "from": "2023-11-01",
            "to": None
        }
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
