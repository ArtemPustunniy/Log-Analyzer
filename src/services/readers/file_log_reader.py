import logging
from datetime import datetime
from pathlib import Path

from src.parsers.nginx_log_parser import NginxLogParser
from src.services.analytics.log_filter import LogFilter
from src.services.readers.log_reader import LogReader


class FileLogReader(LogReader):
    """
    Class for reading log entries from a file and analyzing them.

    The `FileLogReader` reads logs from a specified file path, filters entries
    based on specified criteria, and updates the provided analyzer with relevant
    metrics.
    """

    LOGGER = logging.getLogger("FileLogReader")

    def __init__(self, analyzer):
        """
        Initializes the FileLogReader with a provided analyzer.

        Args:
            analyzer: An object responsible for processing and storing metrics
                      from each log entry.
        """
        self.analyzer = analyzer

    def read_logs(self, file_path, from_time: datetime, to_time: datetime, filter_field: str, filter_value: str) -> None:
        """
        Reads and processes log entries from a specified file.

        This method opens the log file, parses each line, filters entries by time
        and additional filter criteria, and updates the analyzer with valid log data.

        Args:
            file_path (str): The path to the log file.
            from_time (datetime): The starting time for filtering logs.
            to_time (datetime): The ending time for filtering logs.
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
                    after_from = (from_time is None) or (nginx_log.time_local >= from_time.replace(tzinfo=nginx_log.time_local.tzinfo))
                    before_to = (to_time is None) or (nginx_log.time_local <= to_time.replace(tzinfo=nginx_log.time_local.tzinfo))

                    if log_filter.matches_filter(nginx_log, filter_field, filter_value) and after_from and before_to:
                        self.analyzer.update_metrics(nginx_log)
        except IOError:
            self.LOGGER.error(f"Error reading logs from file: {file_path}", exc_info=True)
