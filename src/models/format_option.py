from enum import StrEnum


class FormatOption(StrEnum):
    """
    Enumeration for output format options in log analysis.

    The `FormatOption` enum defines constants for supported output formats,
    such as `markdown` and `adoc` (AsciiDoc).
    """

    MARKDOWN = "markdown"
    ADOC = "adoc"
