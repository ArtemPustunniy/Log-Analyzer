import unittest
from unittest.mock import patch
from src.parsers.paths_parser import PathsParser


class TestPathsParser(unittest.TestCase):
    def setUp(self):
        self.parser = PathsParser()

    @patch("src.parsers.paths_parser.glob.glob")
    @patch("src.parsers.paths_parser.os.path.isfile")
    def test_parse_with_file_paths(self, mock_isfile, mock_glob):
        mock_glob.return_value = ["/path/to/file1.log", "/path/to/file2.log"]
        mock_isfile.side_effect = lambda x: True if x in ["/path/to/file1.log", "/path/to/file2.log"] else False

        path_option = ["/path/to/*.log"]
        result = self.parser.parse(path_option)

        expected_paths = ["/path/to/file1.log", "/path/to/file2.log"]
        self.assertEqual(result, expected_paths)
        mock_glob.assert_called_once_with("/path/to/*.log", recursive=True)

    @patch("src.parsers.paths_parser.glob.glob")
    @patch("src.parsers.paths_parser.os.path.isfile")
    def test_parse_with_mixed_urls_and_file_paths(self, mock_isfile, mock_glob):
        mock_glob.return_value = ["/path/to/file1.log"]
        mock_isfile.side_effect = lambda x: x == "/path/to/file1.log"

        path_option = ["http://example.com", "/path/to/*.log"]
        result = self.parser.parse(path_option)

        expected_paths = ["http://example.com", "/path/to/file1.log"]
        self.assertEqual(result, expected_paths)
        mock_glob.assert_called_once_with("/path/to/*.log", recursive=True)

    def test_parse_with_only_urls(self):
        path_option = ["http://example.com", "https://example.org"]
        result = self.parser.parse(path_option)

        expected_paths = ['http://example.com', 'https://example.org']
        self.assertEqual(result, expected_paths)


if __name__ == '__main__':
    unittest.main()
