import logging
import glob
import os
from typing import List


class PathsParser:
    """
    Class for parsing file paths or URLs from input options.

    The `PathsParser` class provides a method to interpret a dictionary of paths,
    adding valid file paths or URLs to a list. It supports patterns for local
    file paths and checks for file existence.
    """

    LOGGER = logging.getLogger("PathsParser")

    def parse(self, path_option: list) -> List[str]:
        """
        Parses input paths and retrieves valid file paths or URLs.

        This method iterates through the elements in `path_option`. If an element
        is a URL (starts with "http" or "https"), it is added directly to the list.
        If it's a local file pattern, it attempts to match file paths using `glob`,
        adding existing files to the output list. Logs an error if file access
        fails.

        Args:
            path_option (list): A dictionary containing path patterns or URLs.

        Returns:
            List[str]: A list of valid file paths or URLs.
        """
        paths = []
        for elem in path_option:
            if elem.startswith("http://") or elem.startswith("https://"):
                paths.append(elem)
            else:
                try:
                    matched_paths = glob.glob(elem, recursive=True)
                    for path in matched_paths:
                        if os.path.isfile(path):
                            paths.append(path)
                except OSError:
                    self.LOGGER.error("Error: Unable to read files from path pattern.")
        return paths
