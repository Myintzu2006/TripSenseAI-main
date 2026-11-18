import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


DEFAULT_MODEL = "openrouter/free"
FALLBACK_MODELS = (
    "openrouter/free",
    "openai/gpt-oss-20b:free",
    "google/gemma-4-31b-it:free",
)


def _secret(name):
    try:
        import streamlit as st

        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name, "")


def get_api_key():
    return _secret("OPENROUTER_API_KEY").strip()


def get_model():
    return _secret("OPENROUTER_MODEL").strip() or DEFAULT_MODEL


def has_api_key():
    return bool(get_api_key())


def get_client():
    key = get_api_key()
    if not key:
        return None
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=key,
        default_headers={
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Asia Travel Recommender",
        },
    )


def _is_missing_model_error(error):
    text = str(error).lower()
    return "404" in text or "no endpoints found" in text or "not found" in text


def chat_complete(messages, temperature=0.2):
    client = get_client()
    if client is None:
        raise RuntimeError("OpenRouter API key is not set.")

    tried = []
    for model in (get_model(), *FALLBACK_MODELS):
        if model in tried:
            continue
        tried.append(model)
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            return response.choices[0].message.content or ""
        except Exception as error:
            if _is_missing_model_error(error):
                continue
            raise RuntimeError(
                "OpenRouter request failed. Check your API key and try again."
            ) from error

    raise RuntimeError(
        "No working free OpenRouter model is available right now. "
        "Set OPENROUTER_MODEL in .env to another free model from openrouter.ai/models."
    )
