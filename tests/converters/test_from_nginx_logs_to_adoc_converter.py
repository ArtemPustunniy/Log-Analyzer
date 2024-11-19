import unittest
from tempfile import NamedTemporaryFile
from src.converters.from_nginx_logs_to_adoc_converter import FromNginxLogsToAdocConverter
from src.services.readers.file_log_reader import FileLogReader
from src.services.analytics.analyzer import Analyzer
import os


class TestFromNginxLogsToAdocConverterWithFile(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()
        self.converter = FromNginxLogsToAdocConverter()

        self.log_lines = """127.0.0.1 - user1 [19/Nov/2023:10:00:00 +0000] "GET /home HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
127.0.0.1 - user2 [19/Nov/2023:10:05:00 +0000] "GET /about HTTP/1.1" 404 567 "-" "Mozilla/5.0"
127.0.0.1 - user3 [19/Nov/2023:10:10:00 +0000] "GET /contact HTTP/1.1" 500 890 "-" "Mozilla/5.0"
"""

        self.temp_file = NamedTemporaryFile("w+", delete=False)
        self.temp_file.write(self.log_lines)
        self.temp_file.close()

    def test_convert_logs_to_adoc(self):
        log_reader = FileLogReader(self.analyzer)
        log_reader.read_logs(self.temp_file.name, None, None, filter_field=None, filter_value=None)

        report = self.converter.create_a_report(self.analyzer)

        self.assertIn("= Анализ логов Nginx", report)
        self.assertIn("== Общая информация", report)
        self.assertIn("| Начальная дата | 19.11.2023", report)
        self.assertIn("| Конечная дата | 19.11.2023", report)
        self.assertIn("| Количество запросов | 3", report)
        self.assertIn("| Средний размер ответа | 897b", report)
        self.assertIn("| Процент ошибок (4xx и 5xx) | 66.67%", report)

        self.assertIn("== Запрашиваемые ресурсы", report)
        self.assertIn("| /home | 1", report)
        self.assertIn("| /about | 1", report)
        self.assertIn("| /contact | 1", report)

        self.assertIn("== Коды ответа", report)
        self.assertIn("| 200 | OK | 1", report)
        self.assertIn("| 404 | Not Found | 1", report)
        self.assertIn("| 500 | Internal Server Error | 1", report)

    def tearDown(self):
        os.remove(self.temp_file.name)


if __name__ == "__main__":
    unittest.main()
