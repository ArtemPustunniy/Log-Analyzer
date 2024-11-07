import unittest
from datetime import datetime
from unittest.mock import patch
from src.parsers.data_parser import DateParser


class TestDateParser(unittest.TestCase):
    def setUp(self):
        # Создаем экземпляр DateParser для использования в тестах
        self.parser = DateParser()

    def test_valid_date(self):
        # Тестируем корректную дату
        date_str = "2023-01-01"
        parsed_date = self.parser.parse(date_str)
        expected_date = datetime(2023, 1, 1)
        self.assertEqual(parsed_date, expected_date)

    def test_invalid_date_format(self):
        # Тестируем некорректный формат даты
        date_str = "01-01-2023"
        with patch.object(self.parser.LOGGER, 'error') as mock_log_error:
            parsed_date = self.parser.parse(date_str)
            mock_log_error.assert_called_once_with("Error: Invalid date format. Expected format is yyyy-MM-dd")
            self.assertIsNone(parsed_date)

    def test_none_date(self):
        # Тестируем None в качестве даты
        parsed_date = self.parser.parse(None)
        self.assertIsNone(parsed_date)


if __name__ == '__main__':
    unittest.main()
