import unittest
from unittest.mock import patch
from src.parsers.paths_parser import PathsParser


class TestPathsParser(unittest.TestCase):
    def setUp(self):
        # Создаем экземпляр PathsParser для использования в тестах
        self.parser = PathsParser()

    @patch("src.parsers.paths_parser.glob.glob")
    @patch("src.parsers.paths_parser.os.path.isfile")
    def test_parse_with_file_paths(self, mock_isfile, mock_glob):
        # Тестируем обработку локальных файловых путей
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
        # Тестируем обработку комбинации URL и локальных файловых путей
        mock_glob.return_value = ["/path/to/file1.log"]
        mock_isfile.side_effect = lambda x: x == "/path/to/file1.log"

        path_option = ["http://example.com", "/path/to/*.log"]
        result = self.parser.parse(path_option)

        expected_paths = ["http://example.com", "/path/to/file1.log"]
        self.assertEqual(result, expected_paths)
        mock_glob.assert_called_once_with("/path/to/*.log", recursive=True)

    # @patch("src.parsers.paths_parser.os.path.isfile", return_value=False)
    # @patch("src.parsers.paths_parser.glob.glob", return_value=[])
    # @patch("src.parsers.paths_parser.PathsParser.LOGGER")
    # def test_parse_with_invalid_path(self, mock_logger, mock_glob, mock_isfile):
    #     # Тестируем обработку некорректного локального пути, который не соответствует файлам
    #     path_option = ["/invalid/path/*.log"]
    #     result = self.parser.parse(path_option)
    #
    #     self.assertEqual(result, [])
    #     mock_glob.assert_called_once_with("/invalid/path/*.log", recursive=True)
    #     mock_logger.error.assert_called_once_with("Error: Unable to read files from path pattern.")

    def test_parse_with_only_urls(self):
        # Тестируем обработку только URL
        path_option = ["http://example.com", "https://example.org"]
        result = self.parser.parse(path_option)
        # print(result)

        expected_paths = ['http://example.com', 'https://example.org']
        self.assertEqual(result, expected_paths)


if __name__ == '__main__':
    unittest.main()
