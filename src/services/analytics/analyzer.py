from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Set

from src.models.http_status_code import HttpStatusCode

MIN_ERROR_STATUS_CODE = 400
MAX_ERROR_STATUS_CODE = 600


class Analyzer:
    """
    Class for analyzing log data and calculating various metrics.

    The `Analyzer` class processes individual log entries, updating counters,
    tracking unique IPs, calculating error rates, and computing other metrics.
    It can retrieve analyzed data such as 95th percentile response size and
    status code counts.
    """

    def __init__(self):
        """
        Initializes the Analyzer with default counters and storage structures.
        """
        self.count_logs = 0
        self.total_size_logs = 0.0
        self.total_size_count = 0
        self.error_count = 0
        self.unique_ips: Set[str] = set()
        self.response_sizes: List[int] = []
        self.count_status_codes: Dict[int, int] = defaultdict(int)
        self.resource_counts: Dict[str, int] = defaultdict(int)
        self.start_time = None
        self.end_time = None

    def update_metrics(self, log) -> None:
        """
        Updates metrics based on a single log entry.

        This method increments counters for requests, updates response size
        statistics, tracks unique IP addresses, and updates start and end times.

        Args:
            log (NginxLog): A log entry containing data to be analyzed.
        """
        self.count_logs += 1
        self.total_size_logs += log.body_bytes_sent
        self.total_size_count += 1
        self.response_sizes.append(log.body_bytes_sent)

        status_code = log.status
        self.count_status_codes[status_code] += 1

        resource = self.extract_resource_from_request(log.request)
        self.resource_counts[resource] += 1

        self.unique_ips.add(log.remote_addr)

        if MIN_ERROR_STATUS_CODE <= status_code < MAX_ERROR_STATUS_CODE:
            self.error_count += 1

        log_time = log.time_local
        if self.start_time is None or log_time < self.start_time:
            self.start_time = log_time
        if self.end_time is None or log_time > self.end_time:
            self.end_time = log_time

    def extract_resource_from_request(self, request) -> str:
        """
        Extracts the resource path from the request string.

        Args:
            request (str): The request string from which to extract the resource path.

        Returns:
            str: The extracted resource path or the entire request if parsing fails.
        """
        parts = request.split(" ")
        return parts[1] if len(parts) >= 2 else request

    def calculate_95th_percentile(self) -> float:
        """
        Calculates the 95th percentile of response sizes.

        Returns:
            float: The 95th percentile value of response sizes.
        """
        if not self.response_sizes:
            return 0.0
        sorted_sizes = sorted(self.response_sizes)
        index = int(0.95 * len(sorted_sizes)) - 1
        return sorted_sizes[index]

    def get_count_logs(self) -> int:
        """
        Returns the total count of log entries processed.

        Returns:
            int: The number of log entries.
        """
        return self.count_logs

    def get_average_size_logs(self) -> float:
        """
        Calculates the average response size.

        Returns:
            float: The average size of responses, or 0 if no sizes are available.
        """
        return 0 if self.total_size_count == 0 else self.total_size_logs / self.total_size_count

    def get_unique_ip_count(self) -> int:
        """
        Returns the count of unique IP addresses.

        Returns:
            int: The number of unique IP addresses in the logs.
        """
        return len(self.unique_ips)

    def get_error_rate(self) -> float:
        """
        Calculates the error rate as a percentage of total requests.

        Returns:
            float: The error rate in percentage, or 0.0 if no logs are processed.
        """
        return 0.0 if self.count_logs == 0 else (self.error_count / self.count_logs) * 100

    def get_start_date(self) -> (datetime, None):
        """
        Returns the timestamp of the earliest log entry.

        Returns:
            datetime or None: The start time of the logs, or None if unavailable.
        """
        return self.start_time

    def get_end_date(self) -> (datetime, None):
        """
        Returns the timestamp of the latest log entry.

        Returns:
            datetime or None: The end time of the logs, or None if unavailable.
        """
        return self.end_time

    def get_requested_resources(self) -> dict:
        """
        Returns a dictionary of requested resources and their counts.

        Returns:
            dict: A dictionary mapping resource paths to request counts.
        """
        return dict(self.resource_counts)

    def get_status_code_counts(self) -> dict:
        """
        Returns a dictionary of HTTP status codes and their counts.

        Returns:
            dict: A dictionary mapping status codes to their occurrence counts.
        """
        return dict(self.count_status_codes)

    def get_status_code_name(self, status_code) -> str:
        """
        Retrieves the message associated with a specific HTTP status code.

        Args:
            status_code (int): The HTTP status code.

        Returns:
            str: The message for the status code, or "Unknown Status Code" if not found.
        """
        return HttpStatusCode.get_message_by_code(status_code)
