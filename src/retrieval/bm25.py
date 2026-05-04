"""BM25 keyword-based retrieval for Korean particles."""
from bm25s import BM25
import numpy as np
from src.utils.logger import Logger


class BM25Retriever:
    """BM25 retriever optimized for Korean grammar particles."""

    def __init__(self):
        self.logger = Logger("bm25").logger
        self.bm25 = None
        self.corpus = []

    def build_index(self, documents: list[str]):
        """Build BM25 index from document corpus."""
        self.corpus = documents
        tokenized = [doc.split() for doc in documents]
        self.bm25 = BM25()
        self.bm25.index(tokenized)
        self.logger.info(f"BM25 index built with {len(documents)} docs")

    def search(self, query: str, k: int = 5) -> list[tuple[int, float]]:
        """Search and return (doc_index, score) pairs."""
        if not self.bm25:
            return []
        query_tokens = query.split()
        scores = self.bm25.retrieve(query_tokens, k=k)
        return [(idx, score) for idx, score in enumerate(scores.scores[0])]
