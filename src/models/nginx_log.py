from dataclasses import dataclass
from datetime import datetime


@dataclass
class NginxLog:
    """
    Data class representing a single NGINX log entry.

    The `NginxLog` class holds details of an NGINX log entry, including fields
    such as the IP address, request status, and user agent, among others.
    It provides a string representation of the log entry for easy reading.
    """

    remote_addr: str
    remote_user: str
    time_local: datetime
    request: str
    status: int
    body_bytes_sent: int
    http_referer: str
    http_user_agent: str

    def __str__(self) -> str:
        """
        Returns a string representation of the NginxLog object.

        The method formats all log entry details into a readable format,
        ideal for logging or display.

        Returns:
            str: A formatted string containing all log entry fields.
        """
        return (
            f"NginxLog{{"
            f"remoteAddr='{self.remote_addr}', "
            f"remoteUser='{self.remote_user}', "
            f"timeLocal={self.time_local}, "
            f"request='{self.request}', "
            f"status={self.status}, "
            f"bodyBytesSent={self.body_bytes_sent}, "
            f"httpReferer='{self.http_referer}', "
            f"httpUserAgent='{self.http_user_agent}'"
            f"}}"
        )
