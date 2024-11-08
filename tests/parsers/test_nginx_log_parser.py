import unittest
from datetime import datetime, timezone
from unittest.mock import patch
from src.parsers.nginx_log_parser import NginxLogParser
from src.models.nginx_log import NginxLog


class TestNginxLogParser(unittest.TestCase):
    def setUp(self):
        self.parser = NginxLogParser()

    def test_parse_valid_log_line(self):
        log_line = (
            "192.168.0.1 - user123 [01/January/2023:12:00:00 +0000] "
            "\"GET /index.html HTTP/1.1\" 200 1024 "
            "\"http://example.com\" \"Mozilla/5.0\""
        )
        parsed_log = self.parser.parse(log_line)
        expected_log = NginxLog(
            remote_addr="192.168.0.1",
            remote_user="user123",
            time_local=datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            request="GET /index.html HTTP/1.1",
            status=200,
            body_bytes_sent=1024,
            http_referer="http://example.com",
            http_user_agent="Mozilla/5.0"
        )
        self.assertEqual(parsed_log, expected_log)

    def test_parse_invalid_log_format(self):
        log_line = "Invalid log line format"
        with patch.object(self.parser.LOGGER, 'error') as mock_log_error:
            with self.assertRaises(ValueError) as context:
                self.parser.parse(log_line)
            mock_log_error.assert_called_once_with("Incorrect format of log string")
            self.assertEqual(str(context.exception), "Incorrect format of log string")

    def test_parse_invalid_status_format(self):
        log_line = (
            "192.168.0.1 - user123 [01/January/2023:12:00:00 +0000] "
            "\"GET /index.html HTTP/1.1\" ABC 1024 "
            "\"http://example.com\" \"Mozilla/5.0\""
        )
        with patch.object(self.parser.LOGGER, 'error') as mock_log_error:
            with self.assertRaises(ValueError) as context:
                self.parser.parse(log_line)
            mock_log_error.assert_called_once_with("Incorrect format of log string")
            self.assertEqual(str(context.exception), "Incorrect format of log string")

    def test_parse_invalid_body_bytes_sent_format(self):
        log_line = (
            "192.168.0.1 - user123 [01/January/2023:12:00:00 +0000] "
            "\"GET /index.html HTTP/1.1\" 200 XYZ "
            "\"http://example.com\" \"Mozilla/5.0\""
        )
        with patch.object(self.parser.LOGGER, 'error') as mock_log_error:
            with self.assertRaises(ValueError) as context:
                self.parser.parse(log_line)
            mock_log_error.assert_called_once_with("Incorrect format of log string")
            self.assertEqual(str(context.exception), "Incorrect format of log string")

    def test_parse_invalid_time_local_format(self):
        log_line = (
            "192.168.0.1 - user123 [01-01-2023:12:00:00 +0000] "
            "\"GET /index.html HTTP/1.1\" 200 1024 "
            "\"http://example.com\" \"Mozilla/5.0\""
        )
        with patch.object(self.parser.LOGGER, 'error') as mock_log_error:
            with self.assertRaises(ValueError) as context:
                self.parser.parse(log_line)
            mock_log_error.assert_called_once_with("Incorrect format for time_local: %s", "01-01-2023:12:00:00 +0000")
            self.assertEqual(str(context.exception), "Incorrect time format: 01-01-2023:12:00:00 +0000")


if __name__ == '__main__':
    unittest.main()
