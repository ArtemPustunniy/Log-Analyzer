import unittest
from src.parsers.arguments_parser import ArgumentsParser


class TestArgumentsParser(unittest.TestCase):
    def setUp(self):
        self.parser = ArgumentsParser()

    def test_single_value_option(self):
        args = ["--output", "output.txt", "--format", "markdown"]
        parsed_options = self.parser.parse(args)
        expected_options = {
            "output": "output.txt",
            "format": "markdown"
        }
        self.assertEqual(parsed_options, expected_options)

    def test_multiple_value_option(self):
        args = ["--path", "/path/to/log1", "--path", "/path/to/log2"]
        parsed_options = self.parser.parse(args)
        expected_options = {
            "path": ["/path/to/log1", "/path/to/log2"]
        }
        self.assertEqual(parsed_options, expected_options)

    def test_mixed_options(self):
        args = ["--output", "output.txt", "--path", "/path/to/log1", "--path", "/path/to/log2", "--format", "markdown"]
        parsed_options = self.parser.parse(args)
        expected_options = {
            "output": "output.txt",
            "path": ["/path/to/log1", "/path/to/log2"],
            "format": "markdown"
        }
        self.assertEqual(parsed_options, expected_options)

    def test_option_without_value(self):
        args = ["--output"]
        parsed_options = self.parser.parse(args)
        expected_options = {
            "output": None
        }
        self.assertEqual(parsed_options, expected_options)

    def test_no_options(self):
        args = []
        parsed_options = self.parser.parse(args)
        expected_options = {}
        self.assertEqual(parsed_options, expected_options)


if __name__ == '__main__':
    unittest.main()
