#facade/extractor_facade.py

from multiprocessing import Pool
from typing import Callable

from interfaces.repository_interface import RepositoryI
from interfaces.factory_interface import FactoryI

class ExtractionFacade:
    def __init__(
        self,
        app_settings: dict[str, dict],
        repository: Callable[..., RepositoryI],
        factory: FactoryI,
        strategy_mapping: dict[str, type],
        pool_size: int,
    ):
        """
        :param app_settings:      Configurações de extração para cada site (de SETTINGS["app"])  
        :param repository_factory: Classe ou fábrica que cria um RepositoryI c/ **kwargs  
        :param factory_class:     Classe da fábrica de Strategies  
        :param factory_mapping:   Mapeamento de "site_name" para classe de Strategy  
        :param pool_size:         Número de processos paralelos  
        """
        self.app_settings = app_settings
        self.repository = repository
        self.factory = factory
        self.strategy_mapping = strategy_mapping
        self.pool_size = pool_size

    def _execute(self, extractor) -> None:
        """Wrapper para executar extract_data() fora de um lambda (pickle-friendly)"""
        extractor.extract_data()

    def run(self) -> None:
        """
        Cria todos os extractors a partir de app_settings e executa em paralelo.
        """
        extractors = []
        for site_name, site_conf in self.app_settings.items():
            if not isinstance(site_conf, dict):
                continue

            strat_conf = site_conf.get("strategy", {})
            repo_conf = site_conf.get("repository", {})
            # Cria repositório a partir dos parâmetros de repo_conf
            repository = self.repository(**repo_conf)

            # Cria a fábrica injetando repository e mapping
            factory = self.factory(
                repository=repository,
                mapping=self.strategy_mapping
            )

            # Cria o extractor passando só os kwargs válidos
            extractor = factory.create(site_name, **strat_conf)
            extractors.append(extractor)

        # Executa em paralelo
        with Pool(processes=self.pool_size) as pool:
            pool.map(self._execute, extractors)

        print("Todas as extrações concluídas.")