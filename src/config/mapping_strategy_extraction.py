#config/mapping_strategy_extraction.py

from strategies.extraction.inmet_extraction_strategy import InmetExtractionS

STRATETEGY_EXTRACTION_MAPPING: dict[str, type] = {
    "inmet": InmetExtractionS,
}