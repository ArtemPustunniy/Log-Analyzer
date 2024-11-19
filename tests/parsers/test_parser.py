import unittest
from src.parsers.parser import IParser


class TestParserImplementation(IParser):
    def parse(self, input_data):
        return f"Parsed data: {input_data}"


class TestParser(unittest.TestCase):
    def test_parse_method(self):
        parser = TestParserImplementation()
        result = parser.parse("test data")
        self.assertEqual(result, "Parsed data: test data")

    def test_abstract_class_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            IParser()


if __name__ == '__main__':
    unittest.main()
