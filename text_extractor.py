from __future__ import annotations

import os
from typing import Optional

try:
    from PyPDF2 import PdfReader  # type: ignore
except Exception as import_error:  # pragma: no cover
    PdfReader = None  # type: ignore


def extract_text_from_file(file_path: str) -> str:
    """
    Extract plain text from a file.

    Supports .txt and .pdf files.

    - .txt files are read as UTF-8 (invalid bytes ignored)
    - .pdf files are parsed via PyPDF2

    Raises:
        FileNotFoundError: if the path does not exist or is not a file
        ValueError: if the extension is unsupported or PDF parser is unavailable
    """
    if not isinstance(file_path, str) or not file_path:
        raise ValueError("file_path must be a non-empty string")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    _, extension = os.path.splitext(file_path)
    normalized_extension = extension.lower()

    if normalized_extension == ".txt":
        return _extract_text_from_txt(file_path)

    if normalized_extension == ".pdf":
        return _extract_text_from_pdf(file_path)

    raise ValueError(f"Unsupported file extension: {extension}. Only .txt and .pdf are supported.")


def _extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as input_file:
        content = input_file.read()
    return content


def _extract_text_from_pdf(file_path: str) -> str:
    if PdfReader is None:
        raise ValueError(
            "PyPDF2 is required to extract text from PDFs. Please install PyPDF2."
        )

    text_chunks: list[str] = []
    with open(file_path, "rb") as pdf_file:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            page_text: Optional[str] = page.extract_text()  # type: ignore[attr-defined]
            if page_text:
                text_chunks.append(page_text)
    return "\n".join(text_chunks)



