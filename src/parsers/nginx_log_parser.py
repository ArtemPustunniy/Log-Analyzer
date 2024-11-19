import logging
import re

from src.models.nginx_log import NginxLog
from src.parsers.arguments_parser import DateParser
from src.parsers.parser import IParser

LOGGER = logging.getLogger("NginxLogParser")


class NginxLogParser(IParser):
    """
    Class for parsing NGINX log lines into NginxLog objects.

    The `NginxLogParser` class provides functionality to parse log lines from NGINX
    access logs using a regex pattern and convert them into structured `NginxLog`
    objects. It handles errors in individual log fields and logs specific error
    messages when formats are incorrect.
    """

    LOG_PATTERN = (
        r"(?P<remoteAddr>\S+) "
        r"- (?P<remoteUser>\S+) "
        r"\[(?P<timeLocal>.+?)\] "
        r"\"(?P<request>.+?)\" "
        r"(?P<status>\d{3}) "
        r"(?P<bodyBytesSent>\d+) "
        r"\"(?P<httpReferer>.*?)\" "
        r"\"(?P<httpUserAgent>.*?)\""
    )

    def __init__(self):
        """
        Initializes the NginxLogParser with a compiled regex pattern and
        date-time format.
        """
        self.pattern = re.compile(self.LOG_PATTERN)
        self.date_time_formatter = "%d/%B/%Y:%H:%M:%S %z"
        self.date_time_formatter_full = "%d/%b/%Y:%H:%M:%S %z"

    def parse(self, log_line: str) -> NginxLog:
        """
        Parses a single line from an NGINX log file into an NginxLog object.

        This method matches the log line against a regex pattern, extracts
        fields, converts them to the correct types, and handles any parsing
        errors with specific log messages.

        Args:
            log_line (str): A single line from an NGINX log file.

        Returns:
            NginxLog: An instance of the `NginxLog` class with parsed data.

        Raises:
            ValueError: If the log line format is incorrect or if any field
                        fails to parse (e.g., status or body bytes).
        """
        matcher = self.pattern.match(log_line)
        if not matcher:
            LOGGER.error("Incorrect format of log string")
            raise ValueError("Incorrect format of log string")

        remote_addr = matcher.group("remoteAddr")
        remote_user = matcher.group("remoteUser")
        time_local_str = matcher.group("timeLocal")
        request = matcher.group("request")
        http_referer = matcher.group("httpReferer")
        http_user_agent = matcher.group("httpUserAgent")

        try:
            status = int(matcher.group("status"))
        except ValueError:
            LOGGER.error("Incorrect format for status: %s", matcher.group("status"))
            raise ValueError(f"Incorrect format for status: {matcher.group('status')}")

        try:
            body_bytes_sent = int(matcher.group("bodyBytesSent"))
        except ValueError:
            LOGGER.error("Incorrect format for body_bytes_sent: %s", matcher.group("bodyBytesSent"))
            raise ValueError(f"Incorrect format for body_bytes_sent: {matcher.group('bodyBytesSent')}")

        try:
            time_local = DateParser.check_time_pattern(time_local_str)
        except ValueError:
            LOGGER.error("Failed to parse time_local: %s", time_local_str)
            raise ValueError(f"Incorrect time format: {time_local_str}")

        return NginxLog(
            remote_addr,
            remote_user,
            time_local,
            request,
            status,
            body_bytes_sent,
            http_referer,
            http_user_agent
        )
