from http import HTTPStatus


class HttpStatusCode:
    """
    Wrapper for HTTP status codes using the built-in `http.HTTPStatus` module.

    Provides utility methods for accessing HTTP status codes and their messages.
    """

    @staticmethod
    def get_message_by_code(code: int) -> str:
        """
        Retrieves the message for a given HTTP status code.

        Args:
            code (int): The HTTP status code.

        Returns:
            str: The phrase corresponding to the code, or "Unknown Status Code"
                 if the code is not found in the HTTPStatus enumeration.
        """
        try:
            return HTTPStatus(code).phrase
        except ValueError:
            return "Unknown Status Code"
