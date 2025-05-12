#interfaces/repository_interface.py

from abc import ABC, abstractmethod

class RepositoryI(ABC):

    @abstractmethod
    def get_path(self) -> str:
        pass
