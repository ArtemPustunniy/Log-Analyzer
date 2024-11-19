from datetime import datetime

from src.services.analytics.analyzer_intrerface import IAnalyzer
from src.services.readers.file_log_reader import FileLogReader
from src.services.readers.network_log_reader import NetworkLogReader


class LogReaderService:
    """
    Service class for selecting and using the appropriate log reader.

    The `LogReaderService` determines whether to use a file-based log reader or
    a network-based log reader based on the file path prefix and initiates
    the log reading process with the specified filters and analyzer.
    """

    def read_logs(self, file_path: str, from_time: datetime, to_time: datetime, analyzer: IAnalyzer, filter_field: str, filter_value: str) -> None:
        """
        Reads logs from the specified source, selecting the appropriate reader.

        This method chooses between a `FileLogReader` or `NetworkLogReader` based
        on whether the file path starts with "http". It then reads logs from the
        source and applies the specified filters and time range.

        Args:
            file_path (str): The path or URL to the log source.
            from_time (datetime): The start time for filtering logs.
            to_time (datetime): The end time for filtering logs.
            analyzer: An object responsible for analyzing the log data.
            filter_field (str): The field used for filtering logs (e.g., `agent`, `request`, `status`).
            filter_value (str): The value to match within the specified filter field.
        """
        reader = NetworkLogReader(analyzer) if file_path.startswith("http") else FileLogReader(analyzer)
        reader.read_logs(file_path, from_time, to_time, filter_field, filter_value)
