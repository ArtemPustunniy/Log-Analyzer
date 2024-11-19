import argparse
from datetime import datetime


class DateParser:
    """
    A helper class to parse and validate date strings.
    """

    @staticmethod
    def parse(date_str: str) -> (datetime, None):
        """
        Parses a date string in the format 'yyyy-MM-dd'.

        Args:
            date_str (str): The date string to parse.

        Returns:
            datetime: A datetime object if the date is valid, otherwise None.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return None

    @staticmethod
    def check_time_pattern(date_option: str) -> datetime:
        """
        Verifies if a date string matches any predefined formats for NGINX logs.

        Args:
            date_option (str): The date string to check.

        Returns:
            datetime: A parsed `datetime` object if a valid format is found.

        Raises:
            ValueError: If the date string doesn't match any predefined format.
        """
        date_time_formats = [
            "%d/%B/%Y:%H:%M:%S %z",
            "%d/%b/%Y:%H:%M:%S %z",
        ]

        for date_format in date_time_formats:
            try:
                return datetime.strptime(date_option, date_format)
            except ValueError:
                continue

        raise ValueError(f"Incorrect date format: {date_option}")


class ArgumentsParser:
    """
    Wrapper around the argparse.ArgumentParser for parsing command-line arguments.

    This class demonstrates how to use argparse to handle common argument parsing tasks,
    such as handling single and repeated options (e.g., `--path`) and performing additional
    validation for arguments.
    """

    def __init__(self):
        """
        Initializes the argument parser and sets up the arguments.
        """
        self.parser = argparse.ArgumentParser(description="Process command-line arguments.")
        self.parser.add_argument("--path", action="append", help="Specify one or more paths.")
        self.parser.add_argument("--from", help="Specify the start date in yyyy-MM-dd format.")
        self.parser.add_argument("--to", help="Specify the end date in yyyy-MM-dd format.")

    def parse(self, args=None):
        """
        Parses and validates command-line arguments.

        Args:
            args (list, optional): A list of command-line arguments to parse. If not provided,
                                   `argparse` will use `sys.argv`.

        Returns:
            dict or str: A dictionary containing the parsed arguments and their values if valid,
                         or an error message string if validation fails.
        """
        parsed_args = self.parser.parse_args(args)
        options = vars(parsed_args)

        path_option = options.get("path")
        from_option = options.get("from")
        to_option = options.get("to")

        if not path_option:
            return "Error: --path option is required."

        date_parser = DateParser()

        from_date_time = date_parser.parse(from_option) if from_option else None
        if from_option and from_date_time is None:
            return "Error: Invalid date format for --from option. Expected format is yyyy-MM-dd."

        to_date_time = date_parser.parse(to_option) if to_option else None
        if to_option and to_date_time is None:
            return "Error: Invalid date format for --to option. Expected format is yyyy-MM-dd."

        return options
