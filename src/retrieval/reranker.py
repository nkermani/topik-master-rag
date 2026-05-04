# src/retrieval/reranker.py

"""BGE-Reranker for multilingual Korean content."""
from sentence_transformers import CrossEncoder
from src.utils.logger import Logger


class Reranker:
    """Rerank retrieved documents for relevance."""

    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3"):
        self.logger = Logger("reranker").logger
        try:
            self.model = CrossEncoder(model_name)
            self.logger.info(f"Loaded reranker: {model_name}")
        except Exception as e:
            self.logger.error(f"Failed to load reranker: {e}")
            self.model = None

    def rerank(self, query: str, documents: list[str], top_k: int = 5) -> list[int]:
        """Rerank documents and return top-k indices."""
        if not self.model or not documents:
            return list(range(min(top_k, len(documents))))

        pairs = [[query, doc] for doc in documents]
        scores = self.model.predict(pairs)
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return ranked_indices[:top_k]
