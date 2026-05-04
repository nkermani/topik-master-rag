"""Download TOPIK past exam PDFs from topikguide.com."""
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from src.utils.logger import Logger
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class PDFDownloader:
    """Download TOPIK exam PDFs with concurrent downloads."""

    def __init__(self, download_dir: str = "data/raw/pdfs"):
        self.logger = Logger("pdf_downloader").logger
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.base_url = "https://www.topikguide.com"

    def download_all_papers(self, max_workers: int = 5):
        """Scrape and download all available TOPIK papers."""
        pdf_urls = self._scrape_pdf_links()
        self.logger.info(f"Found {len(pdf_urls)} PDFs to download")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self._download_pdf, url): url for url in pdf_urls}
            for future in as_completed(futures):
                url = futures[future]
                try:
                    future.result()
                except Exception as e:
                    self.logger.error(f"Failed {url}: {e}")

    def _scrape_pdf_links(self) -> list[str]:
        """Extract PDF links from topikguide.com pages."""
        pdf_urls = []
        pages = ["/previous-papers/", "/download-35th-topik-test-papers/"]

        for page in pages:
            try:
                response = requests.get(f"{self.base_url}{page}", timeout=10)
                soup = BeautifulSoup(response.content, "html.parser")
                for link in soup.find_all("a", href=True):
                    if link["href"].endswith(".pdf"):
                        pdf_urls.append(link["href"])
            except Exception as e:
                self.logger.error(f"Failed to scrape {page}: {e}")

        return list(set(pdf_urls))  # Remove duplicates

    def _download_pdf(self, url: str):
        """Download a single PDF file."""
        filename = url.split("/")[-1]
        filepath = self.download_dir / filename

        if filepath.exists():
            self.logger.info(f"Already exists: {filename}")
            return

        response = requests.get(url, stream=True, timeout=30)
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        self.logger.info(f"Downloaded: {filename}")
