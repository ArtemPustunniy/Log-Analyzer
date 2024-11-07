import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.services.readers.log_reader_service import LogReaderService


class TestLogReaderService(unittest.TestCase):
    @patch("src.services.readers.log_reader_service.FileLogReader")
    @patch("src.services.readers.log_reader_service.NetworkLogReader")
    def test_read_logs_with_file_reader(self, MockNetworkLogReader, MockFileLogReader):
        # Настройка mock-анализатора
        mock_analyzer = MagicMock()

        # Создаем экземпляр LogReaderService
        service = LogReaderService()

        # Вызов read_logs с локальным файлом
        service.read_logs("local_path.log", datetime(2023, 1, 1), datetime(2023, 1, 2), mock_analyzer, "agent", "Mozilla")

        # Проверка, что был использован FileLogReader, но не NetworkLogReader
        MockFileLogReader.assert_called_once_with(mock_analyzer)
        MockNetworkLogReader.assert_not_called()
        MockFileLogReader.return_value.read_logs.assert_called_once_with(
            "local_path.log", datetime(2023, 1, 1), datetime(2023, 1, 2), "agent", "Mozilla"
        )

    @patch("src.services.readers.log_reader_service.FileLogReader")
    @patch("src.services.readers.log_reader_service.NetworkLogReader")
    def test_read_logs_with_network_reader(self, MockNetworkLogReader, MockFileLogReader):
        # Настройка mock-анализатора
        mock_analyzer = MagicMock()

        # Создаем экземпляр LogReaderService
        service = LogReaderService()

        # Вызов read_logs с URL
        service.read_logs("http://example.com/logs", datetime(2023, 1, 1), datetime(2023, 1, 2), mock_analyzer, "status", "404")

        # Проверка, что был использован NetworkLogReader, но не FileLogReader
        MockNetworkLogReader.assert_called_once_with(mock_analyzer)
        MockFileLogReader.assert_not_called()
        MockNetworkLogReader.return_value.read_logs.assert_called_once_with(
            "http://example.com/logs", datetime(2023, 1, 1), datetime(2023, 1, 2), "status", "404"
        )


if __name__ == '__main__':
    unittest.main()
