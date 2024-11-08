import unittest
from src.models.http_status_code import HttpStatusCode


class TestHttpStatusCode(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(HttpStatusCode.OK.code, 200)
        self.assertEqual(HttpStatusCode.OK.message, "OK")
        self.assertEqual(HttpStatusCode.NOT_FOUND.code, 404)
        self.assertEqual(HttpStatusCode.NOT_FOUND.message, "Not Found")
        self.assertEqual(HttpStatusCode.INTERNAL_SERVER_ERROR.code, 500)
        self.assertEqual(HttpStatusCode.INTERNAL_SERVER_ERROR.message, "Internal Server Error")

    def test_get_message_by_code_existing(self):
        self.assertEqual(HttpStatusCode.get_message_by_code(200), "OK")
        self.assertEqual(HttpStatusCode.get_message_by_code(404), "Not Found")
        self.assertEqual(HttpStatusCode.get_message_by_code(500), "Internal Server Error")

    def test_get_message_by_code_non_existing(self):
        self.assertEqual(HttpStatusCode.get_message_by_code(999), "Unknown Status Code")

    def test_code_and_message_properties(self):
        status = HttpStatusCode.BAD_REQUEST
        self.assertEqual(status.code, 400)
        self.assertEqual(status.message, "Bad Request")


if __name__ == '__main__':
    unittest.main()
