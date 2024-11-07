import logging
from pathlib import Path


class FileLogWriter:
    """
    Class for writing log analysis results to a file.

    The `FileLogWriter` class provides a method to write content (e.g., log analysis
    results) to a specified file. If a file error occurs during writing, an error
    message is logged.
    """

    LOGGER = logging.getLogger("FileLogWriter")

    def write_logs(self, file_name: str, content: str):
        """
        Writes the provided content to a specified file.

        This method opens (or creates if it does not exist) the specified file and
        writes the content into it. If an error occurs while writing, an error
        message is logged.

        Args:
            file_name (str): The name of the file to write to.
            content (str): The content to write to the file.
        """
        path = Path(file_name)
        try:
            with path.open("w", encoding="utf-8") as writer:
                writer.write(content)
        except IOError:
            self.LOGGER.error(f"Error during writing a file: {file_name}", exc_info=True)
