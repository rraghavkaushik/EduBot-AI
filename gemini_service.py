from __future__ import annotations

import hashlib
import os
import threading
import time
from typing import Dict, Tuple

try:
    import google.generativeai as genai  # type: ignore
except Exception:  # pragma: no cover
    genai = None  # type: ignore


_CONFIG_LOCK = threading.Lock()
_IS_CONFIGURED = False


def _configure_once() -> None:
    """
    Configure the Gemini SDK exactly once per process using the `GEMINI_API_KEY` env var.

    Raises:
        RuntimeError: if the SDK is unavailable or the API key is missing.
    """
    global _IS_CONFIGURED
    if _IS_CONFIGURED:
        return
    with _CONFIG_LOCK:
        if _IS_CONFIGURED:
            return
        if genai is None:
            raise RuntimeError(
                "google-generativeai is not installed. Add it to requirements.txt and pip install."
            )
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Export it in your environment before calling Gemini."
            )
        genai.configure(api_key=api_key)
        _IS_CONFIGURED = True


# Simple in-process cache for generations (ephemeral; clears on restart)
_CACHE_TTL_SECONDS = int(os.environ.get("GEMINI_CACHE_TTL_SECONDS", "300"))  # 5 minutes default
_CACHE_MAX_ITEMS = int(os.environ.get("GEMINI_CACHE_MAX_ITEMS", "256"))
_cache_store: Dict[Tuple[str, str], Tuple[float, str]] = {}
_cache_lock = threading.Lock()


def _hash_prompt(prompt: str) -> str:
    # Hash the prompt to keep keys compact. Content-based cache key.
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def _cache_get(model_name: str, prompt: str) -> str | None:
    if _CACHE_TTL_SECONDS <= 0:
        return None
    now = time.time()
    key = (model_name, _hash_prompt(prompt))
    with _cache_lock:
        entry = _cache_store.get(key)
        if not entry:
            return None
        ts, value = entry
        if now - ts > _CACHE_TTL_SECONDS:
            # expired
            _cache_store.pop(key, None)
            return None
        return value


def _cache_put(model_name: str, prompt: str, text: str) -> None:
    if _CACHE_TTL_SECONDS <= 0:
        return
    key = (model_name, _hash_prompt(prompt))
    with _cache_lock:
        # Simple size cap eviction: drop oldest by timestamp when exceeding max items
        if len(_cache_store) >= _CACHE_MAX_ITEMS:
            oldest_key = min(_cache_store.items(), key=lambda kv: kv[1][0])[0]
            _cache_store.pop(oldest_key, None)
        _cache_store[key] = (time.time(), text)


def generate_text_with_gemini(prompt: str, model_name: str | None = None) -> str:
    """
    Generate text from Gemini given a user prompt.

    Args:
        prompt: The user-provided text prompt.
        model_name: Optional model override. Defaults to env `GEMINI_MODEL_NAME` or
            "gemini-1.5-flash" if unset.

    Returns:
        The generated text string.

    Raises:
        RuntimeError: If the SDK/API key is not configured or generation fails.

    Caching notes:
        - This function implements a simple in-process, time-based cache (TTL) keyed by
          (model_name, sha256(prompt)). This avoids recomputing identical generations for a
          period (default 5 minutes). The cache is process-local and ephemeral.
        - For production, prefer an external cache (Redis/Memcached) with:
            key: f"gemini:{model}:{sha256(prompt)}"
            value: generated_text
            TTL: tuned to your freshness/cost needs (e.g., 5–60 minutes)
          You can also cache negative results/timeouts to throttle repeated failures.
        - Consider prompt normalization (trim whitespace, collapse spaces) to increase cache hits.
        - Bust the cache when models are updated or when you roll out new safety/parameters.
    """

    if not isinstance(prompt, str) or not prompt.strip():
        raise RuntimeError("Prompt must be a non-empty string")

    _configure_once()
    model_name = model_name or os.environ.get("GEMINI_MODEL_NAME", "models/gemini-2.0-flash")

    cached = _cache_get(model_name, prompt)
    if cached is not None:
        return cached

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        # Newer SDKs expose `.text`; older may require concatenating parts.
        text = getattr(response, "text", None)
        if not text:
            # Fallback: join candidates content
            text = "".join(getattr(candidate, "content", "") for candidate in getattr(response, "candidates", [])).strip()
        if not text:
            raise RuntimeError("Empty response from Gemini")
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(f"Gemini generation failed: {exc}") from exc

    _cache_put(model_name, prompt, text)
    return text




