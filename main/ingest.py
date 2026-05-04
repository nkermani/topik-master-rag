"""Main entry point for data ingestion."""
import argparse
from src.data.ingest import DataIngestor
from src.utils.logger import Logger


def main():
    """Ingest TOPIK data from various sources."""
    parser = argparse.ArgumentParser(description="Ingest TOPIK data")
    parser.add_argument("--source", choices=["vocab", "past-papers", "all"],
                        default="all", help="Data source to ingest")
    args = parser.parse_args()

    logger = Logger("main_ingest").logger
    ingestor = DataIngestor()

    if args.source in ["vocab", "all"]:
        logger.info("Ingesting vocabulary...")
        vocab = ingestor.ingest_vocab()
        logger.info(f"Total vocabulary items: {len(vocab)}")

    if args.source in ["past-papers", "all"]:
        logger.info("Ingesting PDFs...")
        chunks = ingestor.ingest_pdfs()
        logger.info(f"Total PDF chunks: {len(chunks)}")


if __name__ == "__main__":
    main()
