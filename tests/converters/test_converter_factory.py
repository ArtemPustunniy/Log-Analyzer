import unittest
from src.converters.from_nginx_log_to_markdown_converter import FromNginxLogToMarkDownConverter
from src.converters.from_nginx_logs_to_adoc_converter import FromNginxLogsToAdocConverter
from src.models.format_option import FormatOption
from src.converters.converter_factory import ConverterFactory


class TestConverterFactory(unittest.TestCase):
    def setUp(self):
        self.factory = ConverterFactory()

    def test_markdown_converter_creation(self):
        converter = self.factory.get_converter(FormatOption.MARKDOWN)
        self.assertIsInstance(converter, FromNginxLogToMarkDownConverter)

    def test_adoc_converter_creation(self):
        converter = self.factory.get_converter(FormatOption.ADOC)
        self.assertIsInstance(converter, FromNginxLogsToAdocConverter)

    def test_unsupported_format(self):
        with self.assertRaises(ValueError) as context:
            self.factory.get_converter("unsupported_format")
        self.assertEqual(str(context.exception), "Error: Unsupported format 'unsupported_format'")


if __name__ == '__main__':
    unittest.main()
