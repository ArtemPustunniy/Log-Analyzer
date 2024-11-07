import logging
from datetime import datetime


class DateParser:
    """
    Class for parsing date strings into datetime objects.

    The `DateParser` class provides a method to parse date strings in a specified
    format and convert them into `datetime` objects. It logs an error if the input
    date string does not match the expected format.
    """

    LOGGER = logging.getLogger("DateParser")

    def parse(self, date_option) -> (datetime, None):
        """
        Parses a date string into a `datetime` object.

        This method attempts to convert the provided date string into a `datetime`
        object using the format `yyyy-MM-dd`. If parsing fails due to an invalid
        format, an error is logged and the method returns `None`.

        Args:
            date_option (str): The date string to parse in the format `yyyy-MM-dd`.

        Returns:
            datetime or None: A `datetime` object if parsing is successful; otherwise, `None`.
        """
        if date_option is None:
            return None
        try:
            return datetime.strptime(date_option, "%Y-%m-%d")
        except ValueError:
            self.LOGGER.error("Error: Invalid date format. Expected format is yyyy-MM-dd")
            return None
