# main.py

from factory.site_extractor_factory import ExtractorFactory
from facade.extractor_facade import ExtractionFacade
from repository.local_repository import LocalRepository
from config.settings import SETTINGS
from config.mapping_strategy_extraction import STRATETEGY_EXTRACTION_MAPPING

def main():
    facade = ExtractionFacade(
        app_settings=SETTINGS["app"],
        repository=LocalRepository,
        factory=ExtractorFactory,
        strategy_mapping=STRATETEGY_EXTRACTION_MAPPING,
        pool_size=4,
    )
    facade.run()

if __name__ == "__main__":
    main()
