import unittest

from src.models.filter_field import FilterField


class TestFilterField(unittest.TestCase):
    def test_enum_values(self):
        # Проверяем, что значения перечисления соответствуют ожидаемым строкам
        self.assertEqual(FilterField.AGENT.value, "agent")
        self.assertEqual(FilterField.REQUEST.value, "request")
        self.assertEqual(FilterField.STATUS.value, "status")

    def test_enum_membership(self):
        # Проверяем, что все значения принадлежат FilterField
        self.assertIn("agent", FilterField._value2member_map_)
        self.assertIn("request", FilterField._value2member_map_)
        self.assertIn("status", FilterField._value2member_map_)

    def test_invalid_value(self):
        # Проверяем, что несуществующее значение не принадлежит перечислению
        with self.assertRaises(ValueError):
            FilterField("invalid")


if __name__ == '__main__':
    unittest.main()
