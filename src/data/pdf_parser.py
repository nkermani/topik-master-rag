# src/data/pdf_parser.py

"""PDF parser for TOPIK past exam papers."""
import fitz  # PyMuPDF
from pathlib import Path
from src.utils.logger import Logger


class PDFParser:
    """Extract text from TOPIK exam PDFs."""

    def __init__(self):
        self.logger = Logger("pdf_parser").logger

    def extract_text(self, pdf_path: str) -> list[dict]:
        """Extract text chunks from PDF with metadata."""
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            self.logger.error(f"PDF not found: {pdf_path}")
            return []

        doc = fitz.open(pdf_path)
        chunks = []
        for page_num in range(len(doc)):
            text = doc[page_num].get_text()
            if text.strip():
                chunks.append({
                    "content": text,
                    "source": pdf_path.name,
                    "page": page_num + 1,
                })
        doc.close()
        return chunks
