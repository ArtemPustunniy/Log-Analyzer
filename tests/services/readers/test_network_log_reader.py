import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from src.services.readers.network_log_reader import NetworkLogReader
from src.models.nginx_log import NginxLog


class TestNetworkLogReader(unittest.TestCase):
    def setUp(self):
        self.analyzer = MagicMock()
        self.network_log_reader = NetworkLogReader(self.analyzer)

    @patch("src.services.readers.network_log_reader.requests.get")
    @patch("src.services.readers.network_log_reader.NginxLogParser")
    @patch("src.services.readers.network_log_reader.LogFilter")
    def test_read_logs_valid_response(self, mock_log_filter, mock_nginx_log_parser, mock_requests_get):
        mock_response = MagicMock()
        mock_response.text = (
            "127.0.0.1 - john [19/Nov/2023:15:30:45 +0000] \"GET /index.html HTTP/1.1\" 200 1234 \"-\" \"Mozilla/5.0\"\n"
        )
        mock_response.status_code = 200
        mock_requests_get.return_value = mock_response

        mock_parser_instance = mock_nginx_log_parser.return_value
        mock_log_filter_instance = mock_log_filter.return_value
        mock_parser_instance.parse.return_value = NginxLog(
            remote_addr="127.0.0.1",
            remote_user="john",
            time_local=datetime(2023, 11, 19, 15, 30, 45, tzinfo=timezone.utc),
            request="GET /index.html HTTP/1.1",
            status=200,
            body_bytes_sent=1234,
            http_referer="-",
            http_user_agent="Mozilla/5.0"
        )
        mock_log_filter_instance.matches_filter.return_value = True

        self.network_log_reader.read_logs(
            file_path="http://mockurl.com/logs",
            from_time=datetime(2023, 11, 19, 15, 0, 0, tzinfo=timezone.utc),
            to_time=datetime(2023, 11, 19, 16, 0, 0, tzinfo=timezone.utc),
            filter_field="status",
            filter_value="200"
        )

        mock_requests_get.assert_called_once_with("http://mockurl.com/logs")
        mock_parser_instance.parse.assert_called_once()
        mock_log_filter_instance.matches_filter.assert_called_once()
        self.analyzer.update_metrics.assert_called_once()

    @patch("src.services.readers.network_log_reader.requests.get")
    @patch("src.services.readers.network_log_reader.NginxLogParser")
    @patch("src.services.readers.network_log_reader.LogFilter")
    def test_read_logs_filtering_logic(self, mock_log_filter, mock_nginx_log_parser, mock_requests_get):
        mock_response = MagicMock()
        mock_response.text = (
            "127.0.0.1 - john [19/Nov/2023:15:30:45 +0000] \"GET /index.html HTTP/1.1\" 200 1234 \"-\" \"Mozilla/5.0\"\n"
        )
        mock_response.status_code = 200
        mock_requests_get.return_value = mock_response

        mock_parser_instance = mock_nginx_log_parser.return_value
        mock_log_filter_instance = mock_log_filter.return_value
        mock_parser_instance.parse.return_value = NginxLog(
            remote_addr="127.0.0.1",
            remote_user="john",
            time_local=datetime(2023, 11, 19, 15, 30, 45, tzinfo=timezone.utc),
            request="GET /index.html HTTP/1.1",
            status=200,
            body_bytes_sent=1234,
            http_referer="-",
            http_user_agent="Mozilla/5.0"
        )
        mock_log_filter_instance.matches_filter.return_value = False  # Simulate filtering out

        self.network_log_reader.read_logs(
            file_path="http://mockurl.com/logs",
            from_time=datetime(2023, 11, 19, 15, 0, 0, tzinfo=timezone.utc),
            to_time=datetime(2023, 11, 19, 16, 0, 0, tzinfo=timezone.utc),
            filter_field="status",
            filter_value="404"
        )

        self.analyzer.update_metrics.assert_not_called()


if __name__ == "__main__":
    unittest.main()
