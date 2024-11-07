import unittest

from src.models.format_option import FormatOption


class TestFormatOption(unittest.TestCase):
    def test_enum_values(self):
        # Проверяем, что значения перечисления соответствуют ожидаемым строкам
        self.assertEqual(FormatOption.MARKDOWN.value, "markdown")
        self.assertEqual(FormatOption.ADOC.value, "adoc")

    def test_enum_membership(self):
        # Проверяем, что все значения принадлежат FormatOption
        self.assertIn("markdown", FormatOption._value2member_map_)
        self.assertIn("adoc", FormatOption._value2member_map_)

    def test_invalid_value(self):
        # Проверяем, что несуществующее значение не принадлежит перечислению
        with self.assertRaises(ValueError):
            FormatOption("invalid")


if __name__ == '__main__':
    unittest.main()
