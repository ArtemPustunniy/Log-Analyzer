import unittest
from abc import ABC, abstractmethod


class Converter(ABC):
    @abstractmethod
    def convert(self, analyzer):
        pass


class FakeConverter(Converter):
    """
    A fake converter class for testing purposes.

    Implements the `convert` method, returning a predefined value.
    """

    def convert(self, analyzer):
        # Fake implementation just returns a fixed value for testing purposes
        return f"Converted data from {analyzer}"


class TestConverter(unittest.TestCase):
    def test_cannot_instantiate_converter_directly(self):
        """Test that an instance of Converter cannot be created directly."""
        with self.assertRaises(TypeError):
            Converter()

    def test_can_instantiate_subclass(self):
        """Test that an instance of a subclass of Converter can be created."""
        analyzer = "sample analyzer data"
        converter = FakeConverter()
        result = converter.convert(analyzer)
        self.assertEqual(result, "Converted data from sample analyzer data")


if __name__ == "__main__":
    unittest.main()
