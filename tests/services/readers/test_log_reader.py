import unittest
from datetime import datetime
from src.services.readers.log_reader import LogReader


class TestLogReaderImplementation(LogReader):
    """
    Concrete implementation of the abstract LogReader class for testing purposes.
    """
    def read_logs(self, file_path, from_time, to_time, filter_field, filter_value):
        return f"Read logs from {file_path} with filter {filter_field}={filter_value}"


class TestLogReader(unittest.TestCase):
    def test_read_logs_method(self):
        # Тестируем, что метод read_logs корректно реализован в подклассе
        reader = TestLogReaderImplementation()
        result = reader.read_logs("test.log", datetime(2023, 1, 1), datetime(2023, 1, 2), "agent", "Mozilla")
        expected_result = "Read logs from test.log with filter agent=Mozilla"
        self.assertEqual(result, expected_result)

    def test_abstract_class_cannot_be_instantiated(self):
        # Тестируем, что абстрактный класс LogReader не может быть инстанцирован
        with self.assertRaises(TypeError):
            LogReader()


if __name__ == '__main__':
    unittest.main()
