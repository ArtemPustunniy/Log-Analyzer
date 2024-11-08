import unittest
from unittest.mock import Mock, patch
from src.facades.log_analyzer_facade import LogAnalyzerFacade


class TestLogAnalyzerFacade(unittest.TestCase):
    def setUp(self):
        self.arguments_parser = Mock()
        self.file_log_writer = Mock()
        self.args = Mock()

        self.arguments_parser.parse.return_value = {
            "path": "/path/to/log",
            "from": "2023-01-01",
            "to": "2023-12-31",
            "output": "",
            "format": "markdown",
            "filter-field": "status",
            "filter-value": "404"
        }
        self.facade = LogAnalyzerFacade(self.arguments_parser, self.args)

    @patch("src.facades.log_analyzer_facade.FileLogWriter", return_value=Mock())
    @patch("src.facades.log_analyzer_facade.LogAnalyzerFacade.LOGGER")
    def test_analyze_logs_with_output_option(self, mock_logger, mock_file_log_writer):
        self.arguments_parser.parse.return_value = {
            "path": "/path/to/log",
            "from": None,
            "to": None,
            "output": "/path/to/output.adoc",
            "format": "markdown",
            "filter-field": None,
            "filter-value": None,
        }
        self.facade.analyze_logs()

        mock_file_log_writer.return_value.write_logs.assert_called_once()
        mock_logger.info.assert_not_called()

    @patch("src.facades.log_analyzer_facade.FileLogWriter", return_value=Mock())
    @patch("src.facades.log_analyzer_facade.LogAnalyzerFacade.LOGGER")
    def test_analyze_logs_without_output_option(self, mock_logger, mock_file_log_writer):
        self.arguments_parser.parse.return_value["output"] = ""
        self.facade.analyze_logs()

        mock_logger.info.assert_called_once()
        mock_file_log_writer.return_value.write_logs.assert_not_called()

    @patch("src.facades.log_analyzer_facade.DateParser")
    @patch("src.facades.log_analyzer_facade.PathsParser")
    @patch("src.facades.log_analyzer_facade.Analyzer")
    @patch("src.facades.log_analyzer_facade.LogReaderService")
    @patch("src.facades.log_analyzer_facade.ConverterFactory")
    def test_get_result_analyze(self, mock_converter_factory, mock_log_reader_service, mock_analyzer, mock_paths_parser,
                                mock_date_parser):
        mock_date_parser.return_value.parse.side_effect = lambda x: x  # Возвращает дату как строку
        mock_paths_parser.return_value.parse.return_value = ["/path/to/log"]
        mock_converter = Mock()
        mock_converter.convert.return_value = "Converted data"
        mock_converter_factory.return_value.get_converter.return_value = mock_converter

        result = self.facade.get_result_analyze(
            path_option=["/path/to/log"],
            from_option="2023-01-01",
            to_option="2023-12-31",
            format_option="markdown",
            filter_field="status",
            filter_value="404"
        )

        self.assertEqual(result, "Converted data")
        mock_log_reader_service.return_value.read_logs.assert_called_once_with(
            "/path/to/log",
            "2023-01-01",
            "2023-12-31",
            mock_analyzer.return_value,
            "status",
            "404"
        )
        mock_converter_factory.return_value.get_converter.assert_called_once_with("markdown")
        mock_converter.convert.assert_called_once_with(mock_analyzer.return_value)

    def test_get_result_analyze_missing_path_option(self):
        result = self.facade.get_result_analyze(
            path_option=None,
            from_option="2023-01-01",
            to_option="2023-12-31",
            format_option="markdown",
            filter_field="status",
            filter_value="404"
        )
        self.assertEqual(result, "Error: --path option is required.")

    @patch("src.facades.log_analyzer_facade.DateParser")
    def test_get_result_analyze_invalid_from_date(self, mock_date_parser):
        mock_date_parser.return_value.parse.return_value = None
        result = self.facade.get_result_analyze(
            path_option=["/path/to/log"],
            from_option="invalid-date",
            to_option="2023-12-31",
            format_option="markdown",
            filter_field="status",
            filter_value="404"
        )
        self.assertEqual(result, "Error: Invalid date format for --from option. Expected format is yyyy-MM-dd")

    @patch("src.facades.log_analyzer_facade.DateParser")
    def test_get_result_analyze_invalid_to_date(self, mock_date_parser):
        mock_date_parser.return_value.parse.side_effect = lambda x: None if x == "invalid-date" else x
        result = self.facade.get_result_analyze(
            path_option=["/path/to/log"],
            from_option="2023-01-01",
            to_option="invalid-date",
            format_option="markdown",
            filter_field="status",
            filter_value="404"
        )
        self.assertEqual(result, "Error: Invalid date format for --to option. Expected format is yyyy-MM-dd")


if __name__ == '__main__':
    unittest.main()
