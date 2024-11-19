from abc import ABC, abstractmethod

from src.services.analytics.analyzer_intrerface import IAnalyzer


class IConverter(ABC):
    """
    Abstract base class for converters.

    The `Converter` class defines an interface for all converters,
    requiring them to implement the `convert` method. This method
    accepts an analyzer object and performs a specific conversion,
    which must be implemented in subclasses.
    """

    @abstractmethod
    def create_a_report(self, analyzer: IAnalyzer):
        """
        Abstract method for data conversion.

        This method must be implemented in each subclass of `Converter`.
        It accepts an analyzer object and performs a conversion unique to the subclass.

        """
        pass
