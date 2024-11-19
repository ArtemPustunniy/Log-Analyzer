import logging

from src.converters.converter_factory import ConverterFactory
from src.parsers.data_parser import DateParser
from src.parsers.paths_parser import PathsParser
from src.services.analytics.analyzer import Analyzer
from src.services.readers.log_reader_service import LogReaderService
from src.services.writers.file_log_writer import FileLogWriter

LOGGER = logging.getLogger("FileLogReader")


class LogAnalyzerFacade:
    """
    Facade class for log analysis workflow.

    The `LogAnalyzerFacade` class simplifies the process of analyzing log files by
    orchestrating parsing, filtering, analysis, and conversion of log data based on
    user-specified options. It manages the components necessary for a complete log
    analysis, outputting the results either to a file or the console.
    """

    def __init__(self, arguments_parser, args):
        """
        Initializes the LogAnalyzerFacade with the provided arguments parser and arguments.

        Args:
            arguments_parser: A parser object to interpret command-line arguments.
            args: Command-line arguments for configuring log analysis options.
        """
        self.arguments_parser = arguments_parser
        self.args = args

    def analyze_logs(self) -> None:
        """
        Main method to analyze logs based on command-line arguments.

        This method parses the arguments, retrieves specified options, analyzes logs
        according to filters and date ranges, and either logs the results or writes
        them to an output file based on the user's choice.
        """
        options = self.arguments_parser.parse(self.args)

        path_option = options.get("path")
        from_option = options.get("from")
        to_option = options.get("to")
        output_option = options.get("output", "")
        format_option = options.get("format", "markdown")

        filter_field = options.get("filter-field")
        filter_value = options.get("filter-value")

        result = self.get_result_analyze(path_option, from_option, to_option, format_option, filter_field, filter_value)
        if not output_option:
            LOGGER.info(result)
        else:
            file_log_writer = FileLogWriter()
            file_log_writer.write_logs(output_option, result)

    def get_result_analyze(self, path_option: list, from_option: str, to_option: str, format_option: str, filter_field: str, filter_value: str) -> str:
        """
        Retrieves and analyzes log data based on provided options.

        This method validates the date options, parses paths, applies any specified
        filters, reads log data, and converts the results using the specified format.

        Args:
            path_option (list): The file path(s) for log data.
            from_option (str): Start date for filtering logs.
            to_option (str): End date for filtering logs.
            format_option (str): The desired output format (e.g., markdown or adoc).
            filter_field (str): Log field to filter by.
            filter_value (str): Value to filter in the specified field.

        Returns:
            str: The analyzed and formatted log data as a string, or an error message.
        """
        date_parser = DateParser()

        from_date_time = date_parser.parse(from_option)

        to_date_time = date_parser.parse(to_option)

        paths_parser = PathsParser()
        paths = paths_parser.parse(path_option)

        analyzer = Analyzer()

        log_reader_service = LogReaderService()
        for path in paths:
            log_reader_service.read_logs(
                path,
                from_date_time,
                to_date_time,
                analyzer,
                filter_field,
                filter_value
            )

        converter_factory = ConverterFactory()
        try:
            converter = converter_factory.get_converter(format_option)
        except ValueError:
            return "Error: no such converter"
        return converter.create_a_report(analyzer)
