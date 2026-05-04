# setup.py

from setuptools import setup, find_packages

setup(
    name="topik-master-rag",
    version="0.1.0",
    author="Nathan Kermani",
    author_email="nathan.kermani@example.com",
    description="Level-aware RAG system for TOPIK exam preparation",
    long_description="Level-aware Neural Retrieval system for TOPIK exam preparation. Features Hybrid Search (BM25 + Polyglot-Ko) and Rank-based difficulty filtering.",
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "langchain>=0.1.0",
        "chromadb>=0.4.0",
        "sentence-transformers>=2.2.0",
        "ollama>=0.1.0",
        "PyMuPDF>=1.23.0",
        "ragas>=0.1.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "bm25s>=0.1.0",
        "tqdm>=4.66.0",
        "pyyaml>=6.0.0",
    ],
    extras_require={
        "gpu": ["torch>=2.0.0"],
        "eval": ["ragas[ragas-metrics]>=0.1.0"],
    },
    entry_points={
        "console_scripts": [
            "topik-ingest=main.ingest:main",
            "topik-query=main.query:main",
            "topik-eval=main.eval:main",
            "topik-download=main.download_pdfs:main",
        ],
    },
)
