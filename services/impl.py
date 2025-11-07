from __future__ import annotations
from services.interfaces import TextExtractor, TextGenerator
from text_extractor import extract_text_from_file as _extract
from gemini_service import generate_text_with_gemini as _gen

class DefaultTextExtractor:
    def __call__(self, file_path: str) -> str:
        return _extract(file_path)

class GeminiTextGenerator:
    def __call__(self, prompt: str, model_name: str | None = None) -> str:
        return _gen(prompt, model_name=model_name)
