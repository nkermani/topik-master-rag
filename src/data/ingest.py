"""Main ingestion pipeline for TOPIK data."""
from src.data.scraper import VocabScraper
from src.data.pdf_parser import PDFParser
from src.data.level_tagger import LevelTagger
from src.utils.config import Config
from src.utils.logger import Logger
from pathlib import Path


class DataIngestor:
    """Orchestrate data ingestion from multiple sources."""

    def __init__(self):
        self.config = Config()
        self.logger = Logger("ingestor").logger
        self.scraper = VocabScraper()
        self.parser = PDFParser()
        self.tagger = LevelTagger()

    def ingest_vocab(self):
        """Scrape and store vocabulary for all levels."""
        all_vocab = []
        for level in range(1, 7):
            vocab = self.scraper.scrape_vocab_list(level)
            self.logger.info(f"Scraped {len(vocab)} words for level {level}")
            all_vocab.extend(vocab)
        return all_vocab

    def ingest_pdfs(self):
        """Parse all PDFs in the raw directory."""
        pdf_dir = Path(self.config.get("data.pdf_dir"))
        chunks = []
        for pdf_file in pdf_dir.glob("*.pdf"):
            chunks.extend(self.parser.extract_text(str(pdf_file)))
        self.logger.info(f"Extracted {len(chunks)} chunks from PDFs")
        return chunks
