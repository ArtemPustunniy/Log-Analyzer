import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from src.services.readers.file_log_reader import FileLogReader
from src.models.nginx_log import NginxLog


class TestFileLogReader(unittest.TestCase):
    def setUp(self):
        self.analyzer = MagicMock()
        self.file_log_reader = FileLogReader(self.analyzer)

    @patch("src.services.readers.file_log_reader.Path")
    @patch("src.services.readers.file_log_reader.NginxLogParser")
    @patch("src.services.readers.file_log_reader.LogFilter")
    def test_read_logs_valid_file(self, mock_log_filter, mock_nginx_log_parser, mock_path):
        mock_parser_instance = mock_nginx_log_parser.return_value
        mock_log_filter_instance = mock_log_filter.return_value
        mock_parser_instance.parse.return_value = NginxLog(
            remote_addr="127.0.0.1",
            remote_user="-",
            time_local=datetime(2023, 11, 19, 15, 30, 45, tzinfo=timezone.utc),
            request="GET /index.html HTTP/1.1",
            status=200,
            body_bytes_sent=1234,
            http_referer="-",
            http_user_agent="Mozilla/5.0"
        )
        mock_log_filter_instance.matches_filter.return_value = True

        mock_path_instance = mock_path.return_value
        mock_path_instance.open.return_value.__enter__.return_value = iter([
            "127.0.0.1 - - [19/Nov/2023:15:30:45 +0000] \"GET /index.html HTTP/1.1\" 200 1234 \"-\" \"Mozilla/5.0\""
        ])

        self.file_log_reader.read_logs(
            file_path="mock_file.log",
            from_time=datetime(2023, 11, 19, 15, 0, 0, tzinfo=timezone.utc),
            to_time=datetime(2023, 11, 19, 16, 0, 0, tzinfo=timezone.utc),
            filter_field="status",
            filter_value="200"
        )

        mock_parser_instance.parse.assert_called_once()
        mock_log_filter_instance.matches_filter.assert_called_once()
        self.analyzer.update_metrics.assert_called_once()

    @patch("src.services.readers.file_log_reader.Path")
    @patch("src.services.readers.file_log_reader.LOGGER.error")
    def test_read_logs_file_io_error(self, mock_logger_error, mock_path):
        mock_path_instance = mock_path.return_value
        mock_path_instance.open.side_effect = IOError("File not found")

        self.file_log_reader.read_logs(
            file_path="mock_file.log",
            from_time=None,
            to_time=None,
            filter_field=None,
            filter_value=None
        )

        mock_logger_error.assert_called_once_with(
            "Error reading logs from file: mock_file.log",
            exc_info=True
        )

    def test_is_within_time_range_within_range(self):
        nginx_log = MagicMock()
        nginx_log.time_local = datetime(2023, 11, 19, 15, 30, 45, tzinfo=timezone.utc)
        from_time = datetime(2023, 11, 19, 15, 0, 0, tzinfo=timezone.utc)
        to_time = datetime(2023, 11, 19, 16, 0, 0, tzinfo=timezone.utc)

        result = self.file_log_reader.is_within_time_range(nginx_log, from_time, to_time)
        self.assertTrue(result)

    def test_is_within_time_range_out_of_range(self):
        nginx_log = MagicMock()
        nginx_log.time_local = datetime(2023, 11, 19, 14, 30, 45, tzinfo=timezone.utc)
        from_time = datetime(2023, 11, 19, 15, 0, 0, tzinfo=timezone.utc)
        to_time = datetime(2023, 11, 19, 16, 0, 0, tzinfo=timezone.utc)

        result = self.file_log_reader.is_within_time_range(nginx_log, from_time, to_time)
        self.assertFalse(result)

    def test_is_within_time_range_no_from_time(self):
        nginx_log = MagicMock()
        nginx_log.time_local = datetime(2023, 11, 19, 15, 30, 45, tzinfo=timezone.utc)
        from_time = None
        to_time = datetime(2023, 11, 19, 16, 0, 0, tzinfo=timezone.utc)

        result = self.file_log_reader.is_within_time_range(nginx_log, from_time, to_time)
        self.assertTrue(result)

    def test_is_within_time_range_no_to_time(self):
        nginx_log = MagicMock()
        nginx_log.time_local = datetime(2023, 11, 19, 15, 30, 45, tzinfo=timezone.utc)
        from_time = datetime(2023, 11, 19, 15, 0, 0, tzinfo=timezone.utc)
        to_time = None

        result = self.file_log_reader.is_within_time_range(nginx_log, from_time, to_time)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
