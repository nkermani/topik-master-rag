# src/utils/logger.py

"""Logging utility for TOPIK Master RAG."""
import logging
from pathlib import Path


class Logger:
    """Simple logger setup for the project."""

    def __init__(self, name: str = "topik_rag", log_dir: str = "logs"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        Path(log_dir).mkdir(exist_ok=True)
        if not self.logger.handlers:
            handler = logging.FileHandler(f"{log_dir}/topik_rag.log")
            handler.setFormatter(
                logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            )
            self.logger.addHandler(handler)

    def info(self, msg: str):
        self.logger.info(msg)

    def error(self, msg: str):
        self.logger.error(msg)
