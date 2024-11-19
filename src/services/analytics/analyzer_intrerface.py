from abc import ABC, abstractmethod
from datetime import datetime


class IAnalyzer(ABC):
    """
    Interface for defining required methods for Analyzer and MockAnalyzer.
    """

    @abstractmethod
    def get_start_date(self) -> datetime:
        pass

    @abstractmethod
    def get_end_date(self) -> datetime:
        pass

    @abstractmethod
    def get_count_logs(self) -> int:
        pass

    @abstractmethod
    def get_average_size_logs(self) -> float:
        pass

    @abstractmethod
    def calculate_95th_percentile(self) -> float:
        pass

    @abstractmethod
    def get_unique_ip_count(self) -> int:
        pass

    @abstractmethod
    def get_error_rate(self) -> float:
        pass

    @abstractmethod
    def get_requested_resources(self) -> dict:
        pass

    @abstractmethod
    def get_status_code_counts(self) -> dict:
        pass

    @abstractmethod
    def get_status_code_name(self, code: int) -> str:
        pass
