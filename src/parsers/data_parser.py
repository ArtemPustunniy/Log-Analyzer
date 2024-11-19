import logging
from datetime import datetime

from src.parsers.parser import IParser

LOGGER = logging.getLogger("DateParser")


class DateParser(IParser):
    """
    Class for parsing date strings into datetime objects.

    The `DateParser` class provides methods to parse date strings in specified
    formats and convert them into `datetime` objects. It logs an error if the input
    date string does not match any of the expected formats.
    """

    def __init__(self):
        """
        Initializes the DateParser with common date-time formats.
        """
        self.date_time_formats = [
            "%d/%B/%Y:%H:%M:%S %z",
            "%d/%b/%Y:%H:%M:%S %z",
        ]

    def parse(self, date_option: str) -> datetime | None:
        """
        Parses a date string into a `datetime` object.

        Args:
            date_option (str): The date string to parse.

        Returns:
            datetime or None: A `datetime` object if parsing is successful; otherwise, `None`.
        """
        if not date_option:
            return None
        for date_format in self.date_time_formats:
            try:
                return datetime.strptime(date_option, date_format)
            except ValueError:
                continue
        LOGGER.error("Error: Invalid date format. Expected one of %s", self.date_time_formats)
        return None
