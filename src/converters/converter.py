from abc import ABC, abstractmethod


class Converter(ABC):
    """
    Abstract base class for converters.

    The `Converter` class defines an interface for all converters,
    requiring them to implement the `convert` method. This method
    accepts an analyzer object and performs a specific conversion,
    which must be implemented in subclasses.
    """

    @abstractmethod
    def convert(self, analyzer):
        """
        Abstract method for data conversion.

        This method must be implemented in each subclass of `Converter`.
        It accepts an analyzer object and performs a conversion unique to the subclass.

        Args:
            analyzer: An object representing the analyzer whose data will be converted.
        """
        pass
