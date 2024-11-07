import unittest
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime
from src.services.readers.file_log_reader import FileLogReader
from src.models.nginx_log import NginxLog


class TestFileLogReader(unittest.TestCase):
    @patch("src.services.readers.file_log_reader.Path.open", new_callable=mock_open, read_data="mocked log line")
    @patch("src.services.readers.file_log_reader.NginxLogParser")
    @patch("src.services.readers.file_log_reader.LogFilter")
    def test_read_logs_within_time_range_and_filter(self, MockLogFilter, MockNginxLogParser, mock_open_file):
        # Настройка mock-ов для парсера и фильтра
        mock_parser_instance = MockNginxLogParser.return_value
        mock_log_filter_instance = MockLogFilter.return_value
        mock_analyzer = MagicMock()

        # Создаем тестовые данные
        test_nginx_log = NginxLog(
            remote_addr="192.168.0.1",
            remote_user="user123",
            time_local=datetime(2023, 1, 1, 12, 0, 0),
            request="GET /index.html HTTP/1.1",
            status=200,
            body_bytes_sent=1024,
            http_referer="http://example.com",
            http_user_agent="Mozilla/5.0"
        )

        mock_parser_instance.parse.return_value = test_nginx_log
        mock_log_filter_instance.matches_filter.return_value = True

        # Создаем экземпляр FileLogReader
        file_log_reader = FileLogReader(mock_analyzer)

        # Вызов метода read_logs с временными фильтрами
        from_time = datetime(2023, 1, 1, 11, 0, 0)
        to_time = datetime(2023, 1, 1, 13, 0, 0)
        file_log_reader.read_logs("test.log", from_time, to_time, "agent", "Mozilla")

        # Проверка вызовов методов парсера, фильтра и аналитика
        mock_parser_instance.parse.assert_called_once_with("mocked log line")
        mock_log_filter_instance.matches_filter.assert_called_once_with(test_nginx_log, "agent", "Mozilla")
        mock_analyzer.update_metrics.assert_called_once_with(test_nginx_log)

    @patch("src.services.readers.file_log_reader.Path.open", new_callable=mock_open)
    @patch("src.services.readers.file_log_reader.FileLogReader.LOGGER")
    def test_read_logs_file_io_error(self, mock_logger, mock_open_file):
        # Настройка mock-ов для тестирования IOError
        mock_open_file.side_effect = IOError

        mock_analyzer = MagicMock()
        file_log_reader = FileLogReader(mock_analyzer)

        # Вызов метода read_logs и проверка на логирование ошибки
        file_log_reader.read_logs("invalid_path.log", None, None, None, None)
        mock_logger.error.assert_called_once_with("Error reading logs from file: invalid_path.log", exc_info=True)


if __name__ == '__main__':
    unittest.main()
