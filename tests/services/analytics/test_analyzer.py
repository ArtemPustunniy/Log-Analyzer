import unittest
from datetime import datetime
from unittest.mock import Mock
from src.services.analytics.analyzer import Analyzer
from src.models.nginx_log import NginxLog


class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        # Создаем экземпляр Analyzer для использования в тестах
        self.analyzer = Analyzer()

    def test_update_metrics_single_log(self):
        # Тестируем обновление метрик для одного лога
        log = NginxLog(
            remote_addr="192.168.0.1",
            remote_user="user123",
            time_local=datetime(2023, 1, 1, 12, 0, 0),
            request="GET /index.html HTTP/1.1",
            status=200,
            body_bytes_sent=1024,
            http_referer="http://example.com",
            http_user_agent="Mozilla/5.0"
        )
        self.analyzer.update_metrics(log)

        self.assertEqual(self.analyzer.get_count_logs(), 1)
        self.assertEqual(self.analyzer.get_average_size_logs(), 1024.0)
        self.assertEqual(self.analyzer.get_unique_ip_count(), 1)
        self.assertEqual(self.analyzer.get_error_rate(), 0.0)
        self.assertEqual(self.analyzer.get_start_date(), datetime(2023, 1, 1, 12, 0, 0))
        self.assertEqual(self.analyzer.get_end_date(), datetime(2023, 1, 1, 12, 0, 0))
        self.assertEqual(self.analyzer.get_status_code_counts(), {200: 1})
        self.assertEqual(self.analyzer.get_requested_resources(), {"/index.html": 1})

    def test_update_metrics_multiple_logs(self):
        # Тестируем обновление метрик для нескольких логов
        log1 = NginxLog(
            remote_addr="192.168.0.1",
            remote_user="user123",
            time_local=datetime(2023, 1, 1, 12, 0, 0),
            request="GET /index.html HTTP/1.1",
            status=200,
            body_bytes_sent=1024,
            http_referer="http://example.com",
            http_user_agent="Mozilla/5.0"
        )
        log2 = NginxLog(
            remote_addr="192.168.0.2",
            remote_user="user456",
            time_local=datetime(2023, 1, 1, 13, 0, 0),
            request="POST /submit HTTP/1.1",
            status=404,
            body_bytes_sent=2048,
            http_referer="http://example.com",
            http_user_agent="Mozilla/5.0"
        )

        self.analyzer.update_metrics(log1)
        self.analyzer.update_metrics(log2)

        self.assertEqual(self.analyzer.get_count_logs(), 2)
        self.assertEqual(self.analyzer.get_average_size_logs(), 1536.0)
        self.assertEqual(self.analyzer.get_unique_ip_count(), 2)
        self.assertAlmostEqual(self.analyzer.get_error_rate(), 50.0)
        self.assertEqual(self.analyzer.get_start_date(), datetime(2023, 1, 1, 12, 0, 0))
        self.assertEqual(self.analyzer.get_end_date(), datetime(2023, 1, 1, 13, 0, 0))
        self.assertEqual(self.analyzer.get_status_code_counts(), {200: 1, 404: 1})
        self.assertEqual(self.analyzer.get_requested_resources(), {"/index.html": 1, "/submit": 1})

    from datetime import datetime

    def test_calculate_95th_percentile(self):
        # Тестируем расчет 95-го перцентиля
        sizes = [100, 200, 300, 400, 500, 600]
        for size in sizes:
            log = Mock()
            log.body_bytes_sent = size
            log.request = "GET /test HTTP/1.1"
            log.status = 200
            log.time_local = datetime(2023, 1, 1, 12, 0, 0)
            self.analyzer.update_metrics(log)

        self.assertEqual(self.analyzer.calculate_95th_percentile(), 500)

    def test_extract_resource_from_request(self):
        # Тестируем извлечение ресурса из строки запроса
        request = "GET /test/resource HTTP/1.1"
        resource = self.analyzer.extract_resource_from_request(request)
        self.assertEqual(resource, "/test/resource")

        # Проверка с некорректной строкой запроса
        request = "INVALID REQUEST FORMAT"
        resource = self.analyzer.extract_resource_from_request(request)
        self.assertEqual(resource, "REQUEST")


if __name__ == '__main__':
    unittest.main()
