import unittest
from src.models.http_status_code import HttpStatusCode


class TestHttpStatusCode(unittest.TestCase):
    def test_get_message_by_code_valid(self):
        self.assertEqual(HttpStatusCode.get_message_by_code(200), "OK")
        self.assertEqual(HttpStatusCode.get_message_by_code(404), "Not Found")
        self.assertEqual(HttpStatusCode.get_message_by_code(500), "Internal Server Error")

    def test_get_message_by_code_invalid(self):
        self.assertEqual(HttpStatusCode.get_message_by_code(999), "Unknown Status Code")
        self.assertEqual(HttpStatusCode.get_message_by_code(-1), "Unknown Status Code")
        self.assertEqual(HttpStatusCode.get_message_by_code(600), "Unknown Status Code")

    def test_get_message_by_code_boundary_values(self):
        self.assertEqual(HttpStatusCode.get_message_by_code(100), "Continue")
        self.assertEqual(HttpStatusCode.get_message_by_code(511), "Network Authentication Required")


if __name__ == "__main__":
    unittest.main()
