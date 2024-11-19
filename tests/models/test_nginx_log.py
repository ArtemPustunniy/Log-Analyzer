import unittest
from datetime import datetime
from src.models.nginx_log import NginxLog


class TestNginxLog(unittest.TestCase):
    def setUp(self):
        self.log_entry = NginxLog(
            remote_addr="192.168.0.1",
            remote_user="user123",
            time_local=datetime(2023, 1, 1, 12, 0, 0),
            request="GET /index.html HTTP/1.1",
            status=200,
            body_bytes_sent=1024,
            http_referer="http://example.com",
            http_user_agent="Mozilla/5.0"
        )

    def test_attributes(self):
        self.assertEqual(self.log_entry.remote_addr, "192.168.0.1")
        self.assertEqual(self.log_entry.remote_user, "user123")
        self.assertEqual(self.log_entry.time_local, datetime(2023, 1, 1, 12, 0, 0))
        self.assertEqual(self.log_entry.request, "GET /index.html HTTP/1.1")
        self.assertEqual(self.log_entry.status, 200)
        self.assertEqual(self.log_entry.body_bytes_sent, 1024)
        self.assertEqual(self.log_entry.http_referer, "http://example.com")
        self.assertEqual(self.log_entry.http_user_agent, "Mozilla/5.0")

    def test_str_representation(self):
        expected_str = (
            "NginxLog{remoteAddr='192.168.0.1', "
            "remoteUser='user123', "
            "timeLocal=2023-01-01 12:00:00, "
            "request='GET /index.html HTTP/1.1', "
            "status=200, "
            "bodyBytesSent=1024, "
            "httpReferer='http://example.com', "
            "httpUserAgent='Mozilla/5.0'}"
        )
        self.assertEqual(str(self.log_entry), expected_str)


if __name__ == '__main__':
    unittest.main()
