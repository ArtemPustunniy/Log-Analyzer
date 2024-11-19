import unittest
from unittest.mock import patch
from datetime import datetime
from src.parsers.nginx_log_parser import NginxLogParser
from src.models.nginx_log import NginxLog


class TestNginxLogParser(unittest.TestCase):
    def setUp(self):
        self.parser = NginxLogParser()
        self.valid_log_line = (
            "127.0.0.1 - john [19/Nov/2023:15:30:45 +0000] "
            "\"GET /index.html HTTP/1.1\" 200 1234 \"-\" \"Mozilla/5.0\""
        )

    @patch("src.parsers.nginx_log_parser.DateParser.check_time_pattern")
    def test_parse_valid_log_line(self, mock_date_parser):
        mock_date_parser.return_value = datetime(2023, 11, 19, 15, 30, 45)
        result = self.parser.parse(self.valid_log_line)

        self.assertIsInstance(result, NginxLog)
        self.assertEqual(result.remote_addr, "127.0.0.1")
        self.assertEqual(result.remote_user, "john")
        self.assertEqual(result.time_local, datetime(2023, 11, 19, 15, 30, 45))
        self.assertEqual(result.request, "GET /index.html HTTP/1.1")
        self.assertEqual(result.status, 200)
        self.assertEqual(result.body_bytes_sent, 1234)
        self.assertEqual(result.http_referer, "-")
        self.assertEqual(result.http_user_agent, "Mozilla/5.0")

        mock_date_parser.assert_called_once_with("19/Nov/2023:15:30:45 +0000")

    def test_parse_invalid_log_format(self):
        invalid_log_line = "Invalid log line"
        with self.assertRaises(ValueError) as context:
            self.parser.parse(invalid_log_line)

        self.assertEqual(str(context.exception), "Incorrect format of log string")

    @patch("src.parsers.nginx_log_parser.DateParser.check_time_pattern")
    def test_parse_invalid_status(self, mock_date_parser):
        mock_date_parser.return_value = datetime(2023, 11, 19, 15, 30, 45)
        invalid_status_log = (
            "127.0.0.1 - john [19/Nov/2023:15:30:45 +0000] "
            "\"GET /index.html HTTP/1.1\" INVALID 1234 \"-\" \"Mozilla/5.0\""
        )

        with self.assertRaises(ValueError) as context:
            self.parser.parse(invalid_status_log)

        self.assertEqual(str(context.exception), "Incorrect format of log string")

    @patch("src.parsers.nginx_log_parser.DateParser.check_time_pattern")
    def test_parse_invalid_body_bytes_sent(self, mock_date_parser):
        mock_date_parser.return_value = datetime(2023, 11, 19, 15, 30, 45)
        invalid_body_bytes_log = (
            "127.0.0.1 - john [19/Nov/2023:15:30:45 +0000] "
            "\"GET /index.html HTTP/1.1\" 200 INVALID \"-\" \"Mozilla/5.0\""
        )

        with self.assertRaises(ValueError) as context:
            self.parser.parse(invalid_body_bytes_log)

        self.assertEqual(str(context.exception), "Incorrect format of log string")

    @patch("src.parsers.nginx_log_parser.DateParser.check_time_pattern")
    def test_parse_invalid_time_format(self, mock_date_parser):
        mock_date_parser.side_effect = ValueError("Incorrect time format: Invalid Date")
        invalid_time_log = (
            "127.0.0.1 - john [Invalid Date] "
            "\"GET /index.html HTTP/1.1\" 200 1234 \"-\" \"Mozilla/5.0\""
        )

        with self.assertRaises(ValueError) as context:
            self.parser.parse(invalid_time_log)

        self.assertEqual(str(context.exception), "Incorrect time format: Invalid Date")

    @patch("src.parsers.nginx_log_parser.LOGGER.error")
    def test_parse_logs_error_on_invalid_log(self, mock_logger_error):
        invalid_log_line = "Invalid log line"
        with self.assertRaises(ValueError):
            self.parser.parse(invalid_log_line)

        mock_logger_error.assert_called_once_with("Incorrect format of log string")


if __name__ == "__main__":
    unittest.main()
