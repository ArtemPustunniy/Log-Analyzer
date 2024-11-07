import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.services.readers.network_log_reader import NetworkLogReader
from src.models.nginx_log import NginxLog


class TestNetworkLogReader(unittest.TestCase):
    @patch("src.services.readers.network_log_reader.requests.get")
    @patch("src.services.readers.network_log_reader.NginxLogParser")
    @patch("src.services.readers.network_log_reader.LogFilter")
    def test_read_logs_with_filter_and_time_range(self, MockLogFilter, MockNginxLogParser, mock_requests_get):
        # Настройка mock-ов для парсера и фильтра
        mock_response = MagicMock()
        mock_response.text = "mocked log line\nmocked log line"
        mock_requests_get.return_value = mock_response

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

        # Создаем экземпляр NetworkLogReader
        network_log_reader = NetworkLogReader(mock_analyzer)

        # Вызов метода read_logs с временными фильтрами
        from_time = datetime(2023, 1, 1, 11, 0, 0)
        to_time = datetime(2023, 1, 1, 13, 0, 0)
        network_log_reader.read_logs("http://example.com/logs", from_time, to_time, "agent", "Mozilla")

        # Проверка вызовов методов парсера, фильтра и аналитика
        mock_requests_get.assert_called_once_with("http://example.com/logs")
        mock_parser_instance.parse.assert_called()
        mock_log_filter_instance.matches_filter.assert_called()
        mock_analyzer.update_metrics.assert_called_with(test_nginx_log)

    # @patch("src.services.readers.network_log_reader.requests.get")
    # @patch("src.services.readers.network_log_reader.NetworkLogReader.LOGGER")
    # def test_read_logs_network_error(self, mock_logger, mock_requests_get):
    #     # Настройка mock для тестирования ошибки сети
    #     mock_requests_get.side_effect = requests.RequestException
    #
    #     mock_analyzer = MagicMock()
    #     network_log_reader = NetworkLogReader(mock_analyzer)
    #
    #     # Вызов метода read_logs и проверка на логирование ошибки
    #     network_log_reader.read_logs("http://invalid_url.com/logs", None, None, None, None)
    #     mock_logger.error.assert_called_once_with("Error during network connection to URL: http://invalid_url.com/logs", exc_info=True)


if __name__ == '__main__':
    unittest.main()
