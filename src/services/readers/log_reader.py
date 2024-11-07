from abc import ABC, abstractmethod
from datetime import datetime


class LogReader(ABC):
    """
    Abstract base class for log readers.

    The `LogReader` class defines an interface for reading log entries from a source
    and applying filters based on time range and specific field values.
    Subclasses must implement the `read_logs` method to define the source and
    behavior of log reading.
    """

    @abstractmethod
    def read_logs(self, file_path, from_time: datetime, to_time: datetime, filter_field: str, filter_value: str):
        """
        Abstract method for reading and processing log entries.

        This method should be implemented in subclasses to read logs from the
        specified file path, filter them by time range and additional criteria,
        and perform necessary processing (e.g., updating metrics).

        Args:
            file_path (str): The path to the log file.
            from_time (datetime): The start time for filtering logs.
            to_time (datetime): The end time for filtering logs.
            filter_field (str): The field used for filtering logs (e.g., `agent`, `request`, `status`).
            filter_value (str): The value to match within the specified filter field.
        """
        pass
