"""ChromaDB vector store management."""
import chromadb
from chromadb.config import Settings
from src.utils.config import Config


class VectorStore:
    """Manage ChromaDB persistent storage."""

    def __init__(self):
        self.config = Config()
        self.persist_dir = self.config.get("chroma.persist_directory")
        self.collection_name = self.config.get("chroma.collection_name")
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, docs: list[dict]):
        """Add documents with metadata to vector store."""
        self.collection.add(
            documents=[d["content"] for d in docs],
            metadatas=[d.get("metadata", {}) for d in docs],
            ids=[f"doc_{i}" for i in range(len(docs))]
        )

    def search(self, query: str, filter_dict: dict = None, k: int = 5):
        """Search with optional level filtering."""
        return self.collection.query(
            query_texts=[query],
            n_results=k,
            where=filter_dict
        )
