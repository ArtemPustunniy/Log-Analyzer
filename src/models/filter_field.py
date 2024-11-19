from enum import StrEnum


class FilterField(StrEnum):
    """
    Enumeration for possible filter fields in log analysis.

    The `FilterField` enum defines constants for common fields that can be used
    to filter log data, such as `agent`, `request`, and `status`.
    """

    AGENT = "agent"
    REQUEST = "request"
    STATUS = "status"
