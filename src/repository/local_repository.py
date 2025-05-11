#repository/local_repository.py

from interfaces.repository_interface import RepositoryI

class LocalRepository(RepositoryI):
    def __init__(self, path: str):
        self.path = path

    def get_path(self) -> str:
        return self.path

    def set_path(self, path: str) -> None:
        self.path = path