import unittest

from src.models.format_option import FormatOption


class TestFormatOption(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(FormatOption.MARKDOWN.value, "markdown")
        self.assertEqual(FormatOption.ADOC.value, "adoc")

    def test_enum_membership(self):
        self.assertIn("markdown", FormatOption._value2member_map_)
        self.assertIn("adoc", FormatOption._value2member_map_)

    def test_invalid_value(self):
        with self.assertRaises(ValueError):
            FormatOption("invalid")


if __name__ == '__main__':
    unittest.main()
