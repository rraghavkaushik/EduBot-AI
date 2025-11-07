# solid_examples_codebase.py
from __future__ import annotations
from typing import Protocol, Iterable
import os

"""
SOLID Principles Demo – Industrial-style Refactor
Modules: generators, summarizers, services
Simulates Gemini/Llama API usage for text generation, summarization, and file uploads.
"""

from typing import Protocol
import google.generativeai as genai
from transformers import pipeline
import os

# -----------------------------
# generators.py (LSP)
# -----------------------------
class TextGenerator(Protocol):
    """Protocol for any text-generating model."""
    def __call__(self, prompt: str, model_name: str | None = None) -> str: ...

class GeminiTextGenerator:
    """Actual Gemini LLM API implementation"""
    
    def __init__(self, api_key: str | None = None):
        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable or pass api_key parameter.")
        
        genai.configure(api_key=self.api_key)
    
    def __call__(self, prompt: str, model_name: str | None = None) -> str:
        model_name = model_name or "gemini-1.5-flash"
        
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini Error: {str(e)}"

class LlamaTextGenerator:
    """Actual LLaMA implementation using Hugging Face transformers"""
    
    def __init__(self, model_name: str = "meta-llama/Llama-2-7b-chat-hf"):
        self.default_model = model_name
        self.pipelines = {}
    
    def __call__(self, prompt: str, model_name: str | None = None) -> str:
        model_name = model_name or self.default_model
        
        try:
            # Cache pipelines to avoid reloading models
            if model_name not in self.pipelines:
                self.pipelines[model_name] = pipeline(
                    "text-generation",
                    model=model_name,
                    torch_dtype="auto",
                    device_map="auto"
                )
            
            # Format prompt for LLaMA
            formatted_prompt = f"<s>[INST] {prompt} [/INST]"
            
            # Generate response
            outputs = self.pipelines[model_name](
                formatted_prompt,
                max_new_tokens=256,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
            
            return outputs[0]['generated_text'].replace(formatted_prompt, "").strip()
            
        except Exception as e:
            return f"Llama Error: {str(e)}"

class HuggingFaceTextGenerator:
    """Generic Hugging Face text generator supporting multiple models"""
    
    def __init__(self):
        self.pipelines = {}
    
    def __call__(self, prompt: str, model_name: str | None = None) -> str:
        model_name = model_name or "microsoft/DialoGPT-medium"
        
        try:
            if model_name not in self.pipelines:
                self.pipelines[model_name] = pipeline(
                    "text-generation",
                    model=model_name,
                    torch_dtype="auto",
                    device_map="auto"
                )
            
            outputs = self.pipelines[model_name](
                prompt,
                max_new_tokens=150,
                do_sample=True,
                temperature=0.7
            )
            
            return outputs[0]['generated_text']
            
        except Exception as e:
            return f"HuggingFace Error: {str(e)}"

def produce_answer(generator: TextGenerator, prompt: str) -> str:
    """Work with any LSP-compliant generator."""
    return generator(prompt, model_name=None)






class Summarizer(Protocol):
    """Summarization service interface."""
    def summarize(self, text: str) -> str: ...

class CardMaker(Protocol):
    """Flashcard generation interface."""
    def make_cards(self, text: str, count: int = 5) -> list[tuple[str, str]]: ...

class GeminiSummarizer:
    """Summarizer that calls Gemini API for bullet-style summaries."""
    def __init__(self, generator: TextGenerator):
        self.generator = generator

    def summarize(self, text: str) -> str:
        prompt = f"Summarize the content as concise bullet points:\n{text}"
        raw_output = self.generator(prompt)
        bullets = [f"• {line.strip()}" for line in raw_output.split("\n") if line.strip()]
        return "\n".join(bullets) or "[No summary generated]"

class GeminiCardMaker:
    """Generate flashcards via Gemini API."""
    def __init__(self, generator: TextGenerator):
        self.generator = generator

    def make_cards(self, text: str, count: int = 5) -> list[tuple[str, str]]:
        cards: list[tuple[str, str]] = []
        for i in range(1, count + 1):
            prompt_q = f"Generate REST flashcard Q{i} from:\n{text}"
            prompt_a = f"Generate REST flashcard A{i} from:\n{text}"
            q = self.generator(prompt_q)
            a = self.generator(prompt_a)
            cards.append((q, a))
        return cards

def publish_summary(summarizer: Summarizer, text: str) -> str:
    return summarizer.summarize(text)

def generate_deck(card_maker: CardMaker, text: str, n: int = 3) -> list[tuple[str, str]]:
    return card_maker.make_cards(text, count=n)

# -----------------------------
# services.py (DIP)
# -----------------------------
class TextExtractor(Protocol):
    """Abstraction for file text extraction."""
    def __call__(self, path: str) -> str: ...

class TxtExtractor:
    """Concrete extractor for .txt files"""
    def __call__(self, path: str) -> str:
        if not os.path.exists(path):
            return ""
        if not path.lower().endswith(".txt"):
            return "[Preview unavailable: not a .txt file]"
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            return "[Error reading file]"

class UploadService:
    """High-level service depends on TextExtractor abstraction (DIP)."""
    def __init__(self, extractor: TextExtractor):
        self._extract = extractor

    def handle_upload(self, path: str) -> dict:
        text = self._extract(path)
        preview = text[:120]
        return {"length": len(text), "preview": preview}

# -----------------------------
# main.py (Demo runner)
# -----------------------------
if __name__ == "__main__":
    print("===== LSP =====")
    g1, g2 = GeminiTextGenerator(), LlamaTextGenerator()
    prompt = "Explain idempotency in REST and why PUT is idempotent."
    print(produce_answer(g1, prompt))
    print(produce_answer(g2, prompt))

    print("\n===== ISP =====")
    summarizer = GeminiSummarizer(generator=g1)
    card_maker = GeminiCardMaker(generator=g1)
    text = "REST best practices: methods, status codes, pagination, versioning, authorization."

    print("Summary:\n" + publish_summary(summarizer, text))
    print("\nCards:")
    for i, (q, a) in enumerate(generate_deck(card_maker, text, n=3), 1):
        print(f"{i}. Q: {q}\n   A: {a}")

    print("\n===== DIP =====")
    service = UploadService(TxtExtractor())
    sample_path = "sample_for_upload.txt"
    result = service.handle_upload(sample_path)
    print(f"Preview length: {result['length']}")
    print("Preview snippet:\n" + result["preview"])
