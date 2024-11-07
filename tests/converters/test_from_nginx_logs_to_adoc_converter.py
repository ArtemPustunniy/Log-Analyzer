import unittest
from src.converters.from_nginx_logs_to_adoc_converter import FromNginxLogsToAdocConverter


class MockAnalyzer:
    """
    Mock analyzer to simulate the analyzer's methods and return
    predefined data for testing.
    """

    def get_start_date(self):
        from datetime import datetime
        return datetime(2023, 1, 1)

    def get_end_date(self):
        from datetime import datetime
        return datetime(2023, 12, 31)

    def get_count_logs(self):
        return 15000

    def get_average_size_logs(self):
        return 512.5

    def calculate_95th_percentile(self):
        return 800

    def get_unique_ip_count(self):
        return 1200

    def get_error_rate(self):
        return 2.75

    def get_requested_resources(self):
        return {
            '/home': 5000,
            '/about': 3000,
            '/contact': 2000
        }

    def get_status_code_counts(self):
        return {
            200: 12000,
            404: 2000,
            500: 1000
        }

    def get_status_code_name(self, code):
        names = {
            200: "OK",
            404: "Not Found",
            500: "Internal Server Error"
        }
        return names.get(code, "Unknown")


class TestFromNginxLogsToAdocConverter(unittest.TestCase):
    def setUp(self):
        # Создаем экземпляр конвертера и мок-анализатора
        self.converter = FromNginxLogsToAdocConverter()
        self.analyzer = MockAnalyzer()

    def test_convert_output(self):
        # Тестируем корректность создания AsciiDoc-отчета
        report = self.converter.convert(self.analyzer)

        # Проверка общей информации
        self.assertIn("= Анализ логов Nginx\n\n", report)
        self.assertIn("| Начальная дата | 01.01.2023\n", report)
        self.assertIn("| Конечная дата | 31.12.2023\n", report)
        self.assertIn("| Количество запросов | 15000\n", report)
        self.assertIn("| Средний размер ответа | 512b\n", report)
        self.assertIn("| 95p размера ответа | 800b\n", report)
        self.assertIn("| Количество уникальных IP | 1200\n", report)
        self.assertIn("| Процент ошибок (4xx и 5xx) | 2.75%\n", report)

        # Проверка запрашиваемых ресурсов
        self.assertIn("== Запрашиваемые ресурсы\n\n", report)
        self.assertIn("| /home | 5000\n", report)
        self.assertIn("| /about | 3000\n", report)
        self.assertIn("| /contact | 2000\n", report)

        # Проверка кодов ответа
        self.assertIn("== Коды ответа\n\n", report)
        self.assertIn("| 200 | OK | 12000\n", report)
        self.assertIn("| 404 | Not Found | 2000\n", report)
        self.assertIn("| 500 | Internal Server Error | 1000\n", report)


if __name__ == '__main__':
    unittest.main()
