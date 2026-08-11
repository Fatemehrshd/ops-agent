import os
from dotenv import load_dotenv

load_dotenv(override=True)

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5:7b-instruct")
LLM_API_KEY = os.getenv("LLM_API_KEY", "ollama")
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
CACHE_DIR = os.getenv("CACHE_DIR", "llm_cache")