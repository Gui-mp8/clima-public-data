#interfaces/factory_interface.py

from abc import ABC, abstractmethod

class FactoryI(ABC):
    """
    Abstract Factory Interface
    """

    @abstractmethod
    def create(self, *args, **kwargs):
        """
        Create a new instance of the object.
        """
        pass
