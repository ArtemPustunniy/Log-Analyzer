import unittest
from unittest.mock import patch, mock_open
from src.services.writers.file_log_writer import FileLogWriter


class TestFileLogWriter(unittest.TestCase):
    def setUp(self):
        self.file_writer = FileLogWriter()

    @patch("src.services.writers.file_log_writer.Path.open", new_callable=mock_open)
    def test_write_logs_success(self, mock_file_open):
        file_name = "test_output.log"
        content = "Log analysis results"

        self.file_writer.write_logs(file_name, content)

        mock_file_open.assert_called_once_with("w", encoding="utf-8")
        mock_file_open.return_value.write.assert_called_once_with(content)

    @patch("src.services.writers.file_log_writer.Path.open", new_callable=mock_open)
    def test_write_logs_empty_content(self, mock_file_open):
        file_name = "test_output.log"
        content = ""

        self.file_writer.write_logs(file_name, content)

        mock_file_open.assert_called_once_with("w", encoding="utf-8")
        mock_file_open.return_value.write.assert_called_once_with(content)


if __name__ == "__main__":
    unittest.main()
