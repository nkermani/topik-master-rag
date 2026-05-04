"""Web scraper for TOPIK vocabulary lists."""
import requests
from bs4 import BeautifulSoup
from src.utils.logger import Logger


class VocabScraper:
    """Scrape TOPIK vocabulary with level tags."""

    def __init__(self):
        self.logger = Logger("scraper").logger
        self.base_url = "https://www.topikguide.com"

    def scrape_vocab_list(self, level: int) -> list[dict]:
        """Scrape vocabulary for a specific TOPIK level."""
        url = f"{self.base_url}/topik-vocabulary-level-{level}/"
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            return self._parse_vocab(soup, level)
        except Exception as e:
            self.logger.error(f"Failed to scrape level {level}: {e}")
            return []

    def _parse_vocab(self, soup: BeautifulSoup, level: int) -> list[dict]:
        """Parse vocabulary items from HTML."""
        vocab_items = []
        for item in soup.select(".vocab-item"):
            vocab_items.append({
                "word": item.select_one(".word").text.strip(),
                "meaning": item.select_one(".meaning").text.strip(),
                "topik_level": level,
            })
        return vocab_items
