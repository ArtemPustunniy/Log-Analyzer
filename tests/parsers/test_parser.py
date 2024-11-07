import unittest
from src.parsers.parser import Parser


class TestParserImplementation(Parser):
    """
    Concrete implementation of the abstract Parser class for testing purposes.
    """
    def parse(self, input_data):
        return f"Parsed data: {input_data}"


class TestParser(unittest.TestCase):
    def test_parse_method(self):
        # Тестируем, что метод parse корректно реализован в подклассе
        parser = TestParserImplementation()
        result = parser.parse("test data")
        self.assertEqual(result, "Parsed data: test data")

    def test_abstract_class_cannot_be_instantiated(self):
        # Тестируем, что абстрактный класс Parser не может быть инстанцирован
        with self.assertRaises(TypeError):
            Parser()


if __name__ == '__main__':
    unittest.main()
