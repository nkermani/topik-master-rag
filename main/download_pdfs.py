# main/download_pdfs.py

"""CLI to download TOPIK past exam PDFs."""
import argparse
from src.data.pdf_downloader import PDFDownloader
from src.utils.logger import Logger


def main():
    """Download TOPIK PDFs from topikguide.com."""
    parser = argparse.ArgumentParser(description="Download TOPIK past papers")
    parser.add_argument("--workers", type=int, default=5,
                        help="Concurrent download workers (default: 5)")
    parser.add_argument("--dir", type=str, default="data/raw/pdfs",
                        help="Download directory")
    args = parser.parse_args()

    logger = Logger("main_download").logger
    downloader = PDFDownloader(download_dir=args.dir)

    logger.info("Starting PDF downloads from topikguide.com...")
    downloader.download_all_papers(max_workers=args.workers)
    logger.info("Download complete!")


if __name__ == "__main__":
    main()
