from __future__ import annotations
from typing import Protocol

class TextExtractor(Protocol):
    def __call__(self, file_path: str) -> str: ...

class TextGenerator(Protocol):
    def __call__(self, prompt: str, model_name: str | None = None) -> str: ...

