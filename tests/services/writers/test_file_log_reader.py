import unittest
from unittest.mock import patch, mock_open
from src.services.writers.file_log_writer import FileLogWriter


class TestFileLogWriter(unittest.TestCase):
    @patch("src.services.writers.file_log_writer.Path.open", new_callable=mock_open)
    def test_write_logs_success(self, mock_open_file):
        file_writer = FileLogWriter()

        file_writer.write_logs("test.log", "Test content")

        mock_open_file.assert_called_once_with("w", encoding="utf-8")
        mock_open_file.return_value.write.assert_called_once_with("Test content")

    @patch("src.services.writers.file_log_writer.Path.open", new_callable=mock_open)
    @patch("src.services.writers.file_log_writer.FileLogWriter.LOGGER")
    def test_write_logs_io_error(self, mock_logger, mock_open_file):
        mock_open_file.side_effect = IOError

        file_writer = FileLogWriter()

        file_writer.write_logs("test.log", "Test content")

        mock_logger.error.assert_called_once_with("Error during writing a file: test.log", exc_info=True)


if __name__ == '__main__':
    unittest.main()
