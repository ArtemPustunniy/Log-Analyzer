from datetime import datetime
from pathlib import Path

from src.models.nginx_log import NginxLog
from src.parsers.nginx_log_parser import NginxLogParser
from src.services.analytics.log_filter import LogFilter
from src.services.readers.log_reader import LogReader
import logging

LOGGER = logging.getLogger("FileLogReader")


class FileLogReader(LogReader):
    """
    Class for reading log entries from a file and analyzing them.

    The `FileLogReader` reads logs from a specified file path, filters entries
    based on specified criteria, and updates the provided analyzer with relevant
    metrics.
    """

    def __init__(self, analyzer):
        """
        Initializes the FileLogReader with a provided analyzer.

        Args:
            analyzer: An object responsible for processing and storing metrics
                      from each log entry.
        """
        self.analyzer = analyzer

    def read_logs(self, file_path: str, from_time: datetime | None, to_time: datetime | None, filter_field: str, filter_value: str) -> None:
        """
        Reads and processes log entries from a specified file.

        This method opens the log file, parses each line, filters entries by time
        and additional filter criteria, and updates the analyzer with valid log data.

        Args:
            file_path (str): The path to the log file.
            from_time (datetime | None): The starting time for filtering logs.
            to_time (datetime | None): The ending time for filtering logs.
            filter_field (str): The field to apply filtering on (e.g., `agent`, `request`, `status`).
            filter_value (str): The value to match within the specified filter field.
        """
        path = Path(file_path)
        parser = NginxLogParser()
        log_filter = LogFilter()

        try:
            with path.open("r", encoding="utf-8") as reader:
                for line in reader:
                    nginx_log = parser.parse(line)

                    if (
                        self.is_within_time_range(nginx_log, from_time, to_time)
                        and log_filter.matches_filter(nginx_log, filter_field, filter_value)
                    ):
                        self.analyzer.update_metrics(nginx_log)
        except IOError:
            LOGGER.error(f"Error reading logs from file: {file_path}", exc_info=True)

    def is_within_time_range(self, nginx_log: NginxLog, from_time: datetime | None, to_time: datetime | None) -> bool:
        """
        Checks if the log entry falls within the specified time range.

        Args:
            nginx_log: The log entry object with a `time_local` field.
            from_time (datetime | None): The starting time for filtering logs.
            to_time (datetime | None): The ending time for filtering logs.

        Returns:
            bool: True if the log entry falls within the range, False otherwise.
        """
        if from_time and nginx_log.time_local < from_time.replace(tzinfo=nginx_log.time_local.tzinfo):
            return False
        if to_time and nginx_log.time_local > to_time.replace(tzinfo=nginx_log.time_local.tzinfo):
            return False
        return True
