import logging
import requests
from datetime import datetime

from src.parsers.nginx_log_parser import NginxLogParser
from src.services.analytics.analyzer_intrerface import IAnalyzer
from src.services.analytics.log_filter import LogFilter
from src.services.readers.log_reader import LogReader

LOGGER = logging.getLogger("NetworkLogReader")


class NetworkLogReader(LogReader):
    """
    Class for reading log entries from a network source (URL) and analyzing them.

    The `NetworkLogReader` reads logs from a specified URL, applies filters, and updates
    the provided analyzer with relevant metrics. If a network error occurs, it logs an error.
    """

    def __init__(self, analyzer: IAnalyzer):
        """
        Initializes the NetworkLogReader with a provided analyzer.

        Args:
            analyzer: An object responsible for processing and storing metrics
                      from each log entry.
        """
        self.analyzer = analyzer

    def read_logs(self, file_path: str, from_time: datetime, to_time: datetime, filter_field: str, filter_value: str) -> None:
        """
        Reads and processes log entries from a specified URL.

        This method fetches logs from the URL, parses each line, filters entries by
        time and additional filter criteria, and updates the analyzer with valid log data.

        Args:
            file_path (str): The URL to fetch log data from.
            from_time (datetime): The starting time for filtering logs.
            to_time (datetime): The ending time for filtering logs.
            filter_field (str): The field to apply filtering on (e.g., `agent`, `request`, `status`).
            filter_value (str): The value to match within the specified filter field.
        """
        try:
            response = requests.get(file_path)
            response.raise_for_status()

            parser = NginxLogParser()
            log_filter = LogFilter()

            for line in response.text.splitlines():
                nginx_log = parser.parse(line)
                after_from = (from_time is None) or (nginx_log.time_local >= from_time)
                before_to = (to_time is None) or (nginx_log.time_local <= to_time)

                if log_filter.matches_filter(nginx_log, filter_field, filter_value) and after_from and before_to:
                    self.analyzer.update_metrics(nginx_log)

        except requests.RequestException:
            LOGGER.error(f"Error during network connection to URL: {file_path}", exc_info=True)
