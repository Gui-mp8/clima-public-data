#repository/local_repository.py

from interfaces.repository_interface import RepositoryI

class LocalRepository(RepositoryI):
    def __init__(self, path: str, year: int) -> None:
        self.path = path
        self.year = year

    def get_path(self) -> str:
        return self.path.format(year=self.year)
