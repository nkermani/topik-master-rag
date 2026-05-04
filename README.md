# TOPIK Master: Neural Retrieval System

> **Problem:** Standard LLMs often provide Korean explanations that are too complex or use incorrect honorifics for a learner's specific level.
> **Solution:** A level-aware RAG pipeline that retrieves authentic TOPIK exam patterns and vocabulary, restricted by the user's proficiency level (1-6).

## 🚀 Quick Start

```bash
# Clone and enter the project
git clone https://github.com/nkermani/topik-master-rag.git
cd topik-master-rag

# Set up environment (Option 1: Nix)
nix-shell
pip install -e .

# Or (Option 2: venv)
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Install Ollama for local LLM (optional)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3-korean:8b

# Place TOPIK past exam PDFs in data/raw/pdfs/
# Option A: Manual download from https://www.topikguide.com/topik-past-papers/
# Option B: Auto-download with concurrent scraping (faster!)
topik-download --workers 10

# Ingest TOPIK vocabulary (auto-level-tagged)
topik-ingest --source vocab

# Process past exam PDFs
topik-ingest --source past-papers

# Run a level-filtered query
topik-query "How to use ~기 때문에?" --level 3
```

## 🛠 Tech Stack
- **Orchestration:** LangChain
- **Vector DB:** ChromaDB (Persistent)
- **Embeddings:** `Llama-3-Korean-8B` (Ollama) or `polyglot-ko-1.3b-embeddings`
- **Retrieval:** Ensemble (BM25 + Cosine Similarity)
- **Reranker:** BGE-Reranker-v2 (Multilingual)

## 🚀 Implementation Strategy
### 1. Level-Specific Metadata
Unlike generic RAG, each document in the vector store carries a `topik_level` attribute.
```python
# Search query with level filtering
results = vector_db.similarity_search(
    query="How to use ~기 때문에?",
    filter={"topik_level": {"$lte": 3}} # Only Beginner/Intermediate results
)
```
### 2. Hybrid Retrieval Logic
Korean particles (은/는, 이/가) are functionally critical but semantically "thin" for vectors. We use BM25 to ensure the specific grammar particle the student is asking about is actually present in the retrieved chunks.

### 3. Evaluation (Ragas)
We measure the system's ability to provide a "Correct-Level Explanation" using the Ragas framework, focusing on Faithfulness and Context Precision.

## 📂 Project Structure
```
topik-master-rag/
├── data/
│   ├── raw/             # Unprocessed PDFs, vocab lists
│   └── processed/       # Cleaned, chunked, level-tagged data
├── src/
│   ├── data/            # Ingestion, scraping, parsing scripts
│   ├── retrieval/       # Hybrid search, reranking, LangChain logic
│   ├── evaluation/      # Ragas metrics, benchmarking
│   └── utils/          # Config, logging, helpers
├── configs/             # YAML configs for models, retrieval
├── shell.nix            # Nix environment config
├── setup.py            # Python package setup
└── README.md           # This file
```

## 🛠 Environment Setup
### Option 1: Nix Shell (shell.nix)
For systems with Nix installed, use the provided `shell.nix` to set up the development environment:
```bash
nix-shell
```
This launches a shell with Python 3.10 and core dev tools. Install project dependencies:
```bash
pip install -e .
```

### Option 2: Python venv + setup.py
1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows
```
2. Install the project and dependencies:
```bash
pip install -e .
```

## 📖 How to Use This Repo
1. **Set up the environment** using one of the methods above.
2. **Collect data**:
   - Download past TOPIK exam PDFs from [TOPIK Guide](https://www.topikguide.com/topik-past-papers/) and place them in `data/raw/pdfs/`.
   - Run the vocabulary scraper to auto-tag Level 1-6 vocab:
     ```bash
     topik-ingest --source vocab
     ```
3. **Ingest all data into ChromaDB**:
   ```bash
   topik-ingest --source all
   ```
4. **Run queries** with level filtering:
   ```bash
   topik-query "Explain ~은/는 vs ~이/가" --level 2
   ```
5. **Evaluate performance** with Ragas:
   ```bash
   topik-eval
   ```

## 📂 Data Sources (Free Resources)
- **TOPIK Guide:** Past papers and official vocabulary lists (Level 1-6).
- **KorQuAD:** Korean Question Answering Dataset for machine reading comprehension.
- **AI Hub:** Korean-English Parallel Corpus for colloquial dialogue.

## 🧪 42-Lyon Engineering Focus
- **Resource Constraints:** Optimized to run on a single local GPU (Ollama/Llama-3-8B).
- **Concurrency:** Handling asynchronous retrieval streams for a low-latency UI.

---

### 🛠 Your First Step: Data Collection
To make this work, you need the **Past Papers**. 
1.  Go to [TOPIK Guide](https://www.topikguide.com/topik-past-papers/) and download a few PDFs of past exams.
2.  We will use a Python library called `PyMuPDF` to extract the text.

**Do you want the script to scrape and "Level-Tag" the TOPIK vocabulary lists from the web to start your database?** I can help you write the parser that automatically assigns Level 1-6 tags.
