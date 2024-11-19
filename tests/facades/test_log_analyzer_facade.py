import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

from src.facades.log_analyzer_facade import LogAnalyzerFacade


class TestLogAnalyzerFacade(unittest.TestCase):

    def setUp(self):
        self.arguments_parser = MagicMock()
        self.args = MagicMock()
        self.facade = LogAnalyzerFacade(self.arguments_parser, self.args)

    @patch("src.facades.log_analyzer_facade.DateParser")
    @patch("src.facades.log_analyzer_facade.PathsParser")
    @patch("src.facades.log_analyzer_facade.Analyzer")
    @patch("src.facades.log_analyzer_facade.LogReaderService")
    @patch("src.facades.log_analyzer_facade.ConverterFactory")
    def test_analyze_logs_with_output(self, mock_converter_factory, mock_log_reader_service, mock_analyzer, mock_paths_parser, mock_date_parser):
        self.arguments_parser.parse.return_value = {
            "path": ["log1.txt", "log2.txt"],
            "from": "2023-01-01",
            "to": "2023-01-31",
            "output": "output.md",
            "format": "markdown",
            "filter-field": "status",
            "filter-value": "200"
        }

        mock_date_parser.return_value.parse.side_effect = [
            datetime(2023, 1, 1),
            datetime(2023, 1, 31)
        ]

        mock_paths_parser.return_value.parse.return_value = ["log1.txt", "log2.txt"]
        mock_converter = MagicMock()
        mock_converter.create_a_report.return_value = "Mocked Report"
        mock_converter_factory.return_value.get_converter.return_value = mock_converter
        mock_analyzer.return_value = MagicMock()

        with patch("src.facades.log_analyzer_facade.FileLogWriter") as mock_file_log_writer:
            mock_writer_instance = mock_file_log_writer.return_value
            self.facade.analyze_logs()

            mock_file_log_writer.assert_called_once()
            mock_writer_instance.write_logs.assert_called_once_with("output.md", "Mocked Report")

    @patch("src.facades.log_analyzer_facade.DateParser")
    @patch("src.facades.log_analyzer_facade.PathsParser")
    @patch("src.facades.log_analyzer_facade.Analyzer")
    @patch("src.facades.log_analyzer_facade.LogReaderService")
    @patch("src.facades.log_analyzer_facade.ConverterFactory")
    @patch("src.facades.log_analyzer_facade.LOGGER")
    def test_analyze_logs_without_output(self, mock_logger, mock_converter_factory, mock_log_reader_service, mock_analyzer, mock_paths_parser, mock_date_parser):
        self.arguments_parser.parse.return_value = {
            "path": ["log1.txt"],
            "from": "2023-01-01",
            "to": None,
            "output": "",
            "format": "markdown",
            "filter-field": None,
            "filter-value": None
        }

        mock_date_parser.return_value.parse.side_effect = [
            datetime(2023, 1, 1),
            None
        ]

        mock_paths_parser.return_value.parse.return_value = ["log1.txt"]
        mock_converter = MagicMock()
        mock_converter.create_a_report.return_value = "Mocked Console Report"
        mock_converter_factory.return_value.get_converter.return_value = mock_converter
        mock_analyzer.return_value = MagicMock()

        self.facade.analyze_logs()

        mock_logger.info.assert_called_once_with("Mocked Console Report")

    def test_get_result_analyze_with_invalid_converter(self):
        self.arguments_parser.parse.return_value = {
            "path": ["log1.txt"],
            "from": None,
            "to": None,
            "format": "invalid_format"
        }

        with patch("src.facades.log_analyzer_facade.ConverterFactory") as mock_converter_factory:
            mock_converter_factory.return_value.get_converter.side_effect = ValueError("No such converter")
            result = self.facade.get_result_analyze(["log1.txt"], None, None, "invalid_format", None, None)

            self.assertEqual(result, "Error: no such converter")

    @patch("src.facades.log_analyzer_facade.LogReaderService")
    @patch("src.facades.log_analyzer_facade.DateParser")
    def test_get_result_analyze_valid_case(self, mock_date_parser, mock_log_reader_service):
        mock_date_parser.return_value.parse.side_effect = [datetime(2023, 1, 1), datetime(2023, 1, 31)]
        mock_log_reader_service.return_value.read_logs = MagicMock()

        with patch("src.facades.log_analyzer_facade.ConverterFactory") as mock_converter_factory:
            mock_converter = MagicMock()
            mock_converter.create_a_report.return_value = "Mocked Report"
            mock_converter_factory.return_value.get_converter.return_value = mock_converter

            result = self.facade.get_result_analyze(
                ["log1.txt"],
                "2023-01-01",
                "2023-01-31",
                "markdown",
                None,
                None
            )
            self.assertEqual(result, "Mocked Report")


if __name__ == '__main__':
    unittest.main()
