from src.converters.converter import IConverter
from src.converters.from_nginx_log_to_markdown_converter import FromNginxLogToMarkDownConverter
from src.converters.from_nginx_logs_to_adoc_converter import FromNginxLogsToAdocConverter
from src.models.format_option import FormatOption


class ConverterFactory:
    """
    Factory class to create converter instances based on format options.

    The `ConverterFactory` provides a method to retrieve an appropriate converter
    instance according to the specified format option (e.g., Markdown or AsciiDoc).
    If the format is unsupported, it raises a `ValueError`.
    """

    def get_converter(self, format_option: str) -> IConverter:
        """
        Returns a converter instance based on the format option.

        This method checks the provided format option and returns an instance
        of the appropriate converter class. If the format is not recognized,
        it raises a `ValueError`.

        Args:
            format_option (str): The format option specifying the converter type.
                                 Expected values are defined in `FormatOption`.

        Returns:
            Converter: An instance of the corresponding converter class.

        Raises:
            ValueError: If the format option is unsupported.
        """
        format_option = format_option.lower()
        if format_option == FormatOption.MARKDOWN:
            return FromNginxLogToMarkDownConverter()
        elif format_option == FormatOption.ADOC:
            return FromNginxLogsToAdocConverter()
        else:
            raise ValueError(f"Error: Unsupported format '{format_option}'")
