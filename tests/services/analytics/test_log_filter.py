import unittest
from src.models.nginx_log import NginxLog

from src.models.filter_field import FilterField
from datetime import datetime

from src.services.analytics.log_filter import LogFilter


class TestLogFilter(unittest.TestCase):
    def setUp(self):
        # Создаем экземпляр LogFilter для использования в тестах и тестовый лог
        self.log_filter = LogFilter()
        self.log = NginxLog(
            remote_addr="192.168.0.1",
            remote_user="user123",
            time_local=datetime(2023, 1, 1, 12, 0, 0),
            request="GET /index.html HTTP/1.1",
            status=404,
            body_bytes_sent=1024,
            http_referer="http://example.com",
            http_user_agent="Mozilla/5.0"
        )

    def test_matches_filter_no_filter(self):
        # Тестируем отсутствие фильтра
        self.assertTrue(self.log_filter.matches_filter(self.log, None, None))

    def test_matches_filter_agent(self):
        # Тестируем фильтр по user agent
        self.assertTrue(self.log_filter.matches_filter(self.log, FilterField.AGENT, "Mozilla"))
        self.assertFalse(self.log_filter.matches_filter(self.log, FilterField.AGENT, "Chrome"))

    def test_matches_filter_request(self):
        # Тестируем фильтр по request
        self.assertTrue(self.log_filter.matches_filter(self.log, FilterField.REQUEST, "/index.html"))
        self.assertFalse(self.log_filter.matches_filter(self.log, FilterField.REQUEST, "/contact"))

    def test_matches_filter_status(self):
        # Тестируем фильтр по status
        self.assertTrue(self.log_filter.matches_filter(self.log, FilterField.STATUS, "404"))
        self.assertFalse(self.log_filter.matches_filter(self.log, FilterField.STATUS, "200"))

    def test_matches_filter_invalid_field(self):
        # Тестируем некорректное поле фильтрации
        self.assertFalse(self.log_filter.matches_filter(self.log, "invalid_field", "value"))


if __name__ == '__main__':
    unittest.main()
