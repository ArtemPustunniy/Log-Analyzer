from src.models.filter_field import FilterField


class LogFilter:
    """
    Class for filtering log entries based on specified criteria.

    The `LogFilter` class provides a method to check if a log entry matches a
    specific filter criterion, such as user agent, request, or status code.
    """

    def matches_filter(self, log, filter_field, filter_value) -> bool:
        """
        Checks if a log entry matches the given filter field and value.

        This method compares the specified field and value against the corresponding
        attributes in the log entry. If either `filter_field` or `filter_value` is
        `None`, it returns `True` (i.e., no filtering applied).

        Args:
            log (NginxLog): The log entry to be checked.
            filter_field (str): The field to filter by (e.g., `agent`, `request`, `status`).
            filter_value (str): The value to filter for in the specified field.

        Returns:
            bool: `True` if the log entry matches the filter criteria or if no
                  filtering is applied; `False` otherwise.
        """
        if filter_field is None or filter_value is None:
            return True

        filter_field = filter_field.lower()
        if filter_field == FilterField.AGENT:
            return filter_value in log.http_user_agent
        elif filter_field == FilterField.REQUEST:
            return filter_value in log.request
        elif filter_field == FilterField.STATUS:
            return str(log.status) == filter_value
        else:
            return False
