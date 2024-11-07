import unittest
from unittest.mock import patch, mock_open
from src.services.writers.file_log_writer import FileLogWriter


class TestFileLogWriter(unittest.TestCase):
    @patch("src.services.writers.file_log_writer.Path.open", new_callable=mock_open)
    def test_write_logs_success(self, mock_open_file):
        # Создаем экземпляр FileLogWriter
        file_writer = FileLogWriter()

        # Вызов метода write_logs с тестовыми данными
        file_writer.write_logs("test.log", "Test content")

        # Проверка, что файл был открыт для записи и данные записаны
        mock_open_file.assert_called_once_with("w", encoding="utf-8")
        mock_open_file.return_value.write.assert_called_once_with("Test content")

    @patch("src.services.writers.file_log_writer.Path.open", new_callable=mock_open)
    @patch("src.services.writers.file_log_writer.FileLogWriter.LOGGER")
    def test_write_logs_io_error(self, mock_logger, mock_open_file):
        # Настройка mock для выбрасывания IOError
        mock_open_file.side_effect = IOError

        # Создаем экземпляр FileLogWriter
        file_writer = FileLogWriter()

        # Вызов метода write_logs, который должен вызвать ошибку
        file_writer.write_logs("test.log", "Test content")

        # Проверка, что был зарегистрирован вызов метода error при IOError
        mock_logger.error.assert_called_once_with("Error during writing a file: test.log", exc_info=True)


if __name__ == '__main__':
    unittest.main()
