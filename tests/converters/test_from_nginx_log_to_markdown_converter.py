import unittest
from unittest.mock import MagicMock, patch
from tempfile import NamedTemporaryFile
from datetime import datetime, timezone
from src.converters.from_nginx_log_to_markdown_converter import FromNginxLogToMarkDownConverter
from src.services.readers.file_log_reader import FileLogReader
from src.services.analytics.analyzer import Analyzer
import os


class TestFromNginxLogToMarkDownConverterWithFile(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()
        self.converter = FromNginxLogToMarkDownConverter()

        self.log_lines = """127.0.0.1 - user1 [19/Nov/2023:10:00:00 +0000] "GET /home HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
127.0.0.1 - user2 [19/Nov/2023:10:05:00 +0000] "GET /about HTTP/1.1" 404 567 "-" "Mozilla/5.0"
127.0.0.1 - user3 [19/Nov/2023:10:10:00 +0000] "GET /contact HTTP/1.1" 500 890 "-" "Mozilla/5.0"
"""

        self.temp_file = NamedTemporaryFile("w+", delete=False)
        self.temp_file.write(self.log_lines)
        self.temp_file.close()

    @patch("src.parsers.nginx_log_parser.NginxLogParser.parse")
    def test_convert_logs_to_markdown(self, mock_parser):
        mock_parser.side_effect = [
            MagicMock(
                remote_addr="127.0.0.1",
                remote_user="user1",
                time_local=datetime(2023, 11, 19, 10, 0, 0, tzinfo=timezone.utc),
                request="GET /home HTTP/1.1",
                status=200,
                body_bytes_sent=1234,
                http_referer="-",
                http_user_agent="Mozilla/5.0",
            ),
            MagicMock(
                remote_addr="127.0.0.1",
                remote_user="user2",
                time_local=datetime(2023, 11, 19, 10, 5, 0, tzinfo=timezone.utc),
                request="GET /about HTTP/1.1",
                status=404,
                body_bytes_sent=567,
                http_referer="-",
                http_user_agent="Mozilla/5.0",
            ),
            MagicMock(
                remote_addr="127.0.0.1",
                remote_user="user3",
                time_local=datetime(2023, 11, 19, 10, 10, 0, tzinfo=timezone.utc),
                request="GET /contact HTTP/1.1",
                status=500,
                body_bytes_sent=890,
                http_referer="-",
                http_user_agent="Mozilla/5.0",
            ),
        ]

        log_reader = FileLogReader(self.analyzer)
        log_reader.read_logs(self.temp_file.name, None, None, filter_field=None, filter_value=None)

        report = self.converter.create_a_report(self.analyzer)

        self.assertIn("#### Общая информация", report)
        self.assertIn("|  Количество запросов  |       3 |", report)
        self.assertIn("| Средний размер ответа |         897b |", report)
        self.assertIn("| Процент ошибок (4xx и 5xx) |       66.67% |", report)
        self.assertIn("#### Запрашиваемые ресурсы", report)
        self.assertIn("|  `/home`  |      1 |", report)
        self.assertIn("|  `/about`  |      1 |", report)
        self.assertIn("|  `/contact`  |      1 |", report)
        self.assertIn("#### Коды ответа", report)
        self.assertIn("| 200 | OK |       1 |", report)
        self.assertIn("| 404 | Not Found |       1 |", report)
        self.assertIn("| 500 | Internal Server Error |       1 |", report)

    def tearDown(self):
        os.remove(self.temp_file.name)


if __name__ == "__main__":
    unittest.main()
