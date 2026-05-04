# src/retrieval/embeddings.py

"""Embedding models for Korean text."""
from sentence_transformers import SentenceTransformer
from src.utils.config import Config
from src.utils.logger import Logger


class EmbeddingModel:
    """Load and use Korean embedding models."""

    def __init__(self):
        self.config = Config()
        self.logger = Logger("embeddings").logger
        self.model_name = self.config.get("embeddings.model_name", "polyglot-ko-1.3b")
        self.model = None

    def load(self):
        """Load the embedding model."""
        try:
            self.model = SentenceTransformer(self.model_name)
            self.logger.info(f"Loaded embedding model: {self.model_name}")
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise

    def encode(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for texts."""
        if not self.model:
            self.load()
        return self.model.encode(texts).tolist()
