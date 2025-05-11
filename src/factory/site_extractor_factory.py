# factory/site_extractor_factory.py
import inspect
from interfaces.factory_interface import FactoryI
from interfaces.extraction_strategy_interface import ExtractionSI
from interfaces.repository_interface import RepositoryI

class ExtractorFactory(FactoryI):

    def __init__(self, repository: RepositoryI, mapping: dict[str, type[ExtractionSI]]):
        self.repository = repository
        self.mapping = mapping

    def create(self, site_name: str, **kwargs) -> ExtractionSI:
        try:
            extractor_cls = self.mapping[site_name]
        except KeyError:
            raise ValueError(f"Extractor para '{site_name}' não encontrado")

        # filtra só os kwargs que o __init__ do extractor aceita
        params = inspect.signature(extractor_cls).parameters
        valid_kwargs = {
            k: v for k, v in kwargs.items()
            if k in params and k != "self"
        }

        return extractor_cls(repository=self.repository, **valid_kwargs)
