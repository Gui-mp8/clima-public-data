#interfaces/extraction_strategy_interface.py

from abc import ABC, abstractmethod

class ExtractionSI(ABC):
    def __init__(self):
        self._url = None

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str) -> None:

        self._url = value

    @abstractmethod
    def extract_data(self) -> None:
        """
        Extracts data from the given source.
        """
        pass