import unittest
from abc import ABC, abstractmethod


class Converter(ABC):
    @abstractmethod
    def convert(self, analyzer):
        pass


class FakeConverter(Converter):

    def convert(self, analyzer):
        return f"Converted data from {analyzer}"


class TestConverter(unittest.TestCase):
    def test_cannot_instantiate_converter_directly(self):
        with self.assertRaises(TypeError):
            Converter()

    def test_can_instantiate_subclass(self):
        analyzer = "sample analyzer data"
        converter = FakeConverter()
        result = converter.convert(analyzer)
        self.assertEqual(result, "Converted data from sample analyzer data")


if __name__ == "__main__":
    unittest.main()
