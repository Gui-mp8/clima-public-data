from abc import ABC, abstractmethod

class RepositoryI(ABC):

    @abstractmethod
    def get_path(self) -> str:
        pass

    @abstractmethod
    def set_path(self, path: str) -> None:
        pass