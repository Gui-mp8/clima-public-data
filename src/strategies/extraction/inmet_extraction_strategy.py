#strategies/extraction/inmet_extraction_strategy.py

import zipfile
from io import BytesIO

import requests

from interfaces.extraction_strategy_interface import ExtractionSI
from interfaces.repository_interface import RepositoryI


class InmetExtractionS(ExtractionSI):
    def __init__(self, repository: RepositoryI, url: str, year: int, cities: list[str]):
        self.repository = repository
        self.url = url
        self.cities = cities
        self.year = year
    """
    InmetExtractionS is a class that implements the ExtractionSI interface for extracting data from the INMET API.
    """
    def _get_response(self, url: str) -> bytes:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.content
            else:
                raise Exception(f"Failed to fetch data from INMET API. Status code: {response.status_code}")

        except requests.RequestException as e:
            raise Exception(f"An error occurred while making the request: {e}")


    def extract_data(self) -> None:
        """
        Extracts data from the INMET SITE.
        """
        url = self.url.format(year=self.year)
        
        zip_bytes = self._get_response(url)

        with zipfile.ZipFile(BytesIO(zip_bytes)) as zip_ref:
            all_files = zip_ref.namelist()
            
            # Filtra arquivos em memoria por cidade
            matched_files = [
                file for file in all_files
                if any(city.lower() in file.lower() for city in self.cities)
            ]

            for filename in matched_files:
                zip_ref.extract(filename, path=self.repository.get_path())

