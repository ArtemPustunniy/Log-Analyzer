from abc import ABC, abstractmethod


class IParser(ABC):
    """
    Abstract base class for parsers.

    The `Parser` class defines an interface for parsing data, requiring subclasses
    to implement the `parse` method, which takes input data and processes it in a
    specific way.
    """

    @abstractmethod
    def parse(self, input_data: str):
        """
        Abstract method for parsing input data.

        This method must be implemented in each subclass to define the specific
        parsing logic based on the type of input data provided.

        Args:
            input_data: The data to be parsed by the parser.

        Returns:
            The result of the parsing process, as defined by the subclass.
        """
        pass
