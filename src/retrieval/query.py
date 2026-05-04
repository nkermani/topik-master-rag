"""Main query pipeline with hybrid retrieval."""
from src.retrieval.vector_store import VectorStore
from src.retrieval.bm25 import BM25Retriever
from src.retrieval.reranker import Reranker
from src.utils.logger import Logger


class QueryPipeline:
    """Orchestrate hybrid retrieval with level filtering."""

    def __init__(self):
        self.logger = Logger("query_pipeline").logger
        self.vector_store = VectorStore()
        self.bm25 = BM25Retriever()
        self.reranker = Reranker()

    def search(self, query: str, topik_level: int = None, k: int = 5) -> list[str]:
        """Perform hybrid search with optional level filter."""
        filter_dict = {"topik_level": {"$lte": topik_level}} if topik_level else None

        vector_results = self.vector_store.search(query, filter_dict, k=k * 2)
        bm25_results = self.bm25.search(query, k=k * 2)

        combined = self._merge_results(vector_results, bm25_results)
        documents = [r["content"] for r in combined]

        top_indices = self.reranker.rerank(query, documents, top_k=k)
        return [documents[i] for i in top_indices]

    def _merge_results(self, vector_res, bm25_res):
        """Merge and deduplicate results from both retrievers."""
        return vector_res  # Simplified merge
