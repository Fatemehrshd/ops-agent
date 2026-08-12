from dataclasses import dataclass, field
from typing import Any
import hashlib
import json
from pathlib import Path
from openai import OpenAI
import logging
import time
from pydantic import BaseModel

from test import response

from . import config

_client = OpenAI(base_url=config.LLM_BASE_URL, api_key=config.LLM_API_KEY)

logger = logging.getLogger(__name__)

@dataclass
class LLMResponse:
    text: str
    prompt_tokens: int
    completion_tokens: int
    latency_s: float
    model: str
    wall_time_s: float = 0.0
    cached: bool = False
    tool_calls: list[dict[str, Any]] = field(default_factory=list),
    parsed: Any | None = None

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    @property
    def cost_usd(self) -> float:
        return 0.0

def _cache_key(payload: dict) -> str:
    json_string = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    hashed = hashlib.sha256(json_string.encode()).hexdigest()[:32]
    return hashed

def _cache_read(key: str) -> dict | None:
    if not config.CACHE_ENABLED:
        return None

    path = Path(config.CACHE_DIR) / f"{key}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))
    
def _cache_write(key: str, data: dict) -> None:
    if not config.CACHE_ENABLED:
        return
    dir = Path(config.CACHE_DIR)
    dir.mkdir(parents=True, exist_ok=True)
    file_path = dir / f"{key}.json"
    file_path.write_text(
        json.dumps(data, ensure_ascii=False, sort_keys=True), encoding="utf-8"
    )


def chat(
    messages: list[dict],
    tools: list[dict] | None = None,
    temperature: float = 0.0,
    max_tokens: int = 800,
    model: str | None = None,
    response_format: type[BaseModel] | None = None,
) -> LLMResponse:

    started_at = time.perf_counter()
    model = model or config.LLM_MODEL
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    if tools:
        payload["tools"] = tools
    
    if response_format is not None:
        payload["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": response_format.__name__,
                "schema": response_format.model_json_schema()
            },
        }

    key = _cache_key(payload)
    hit = _cache_read(key)

    if hit is not None:
        wall_time = round(time.perf_counter() - started_at, 4)

        parsed = None

        if response_format is not None:
            parsed = response_format.model_validate_json(hit["text"])

        logger.info(json.dumps(
            {"event": "llm_call",
            "cached": True,
            "model": model,
            "wall_time_s": wall_time,
        }))

        return LLMResponse(
            **hit, 
            cached=True, 
            wall_time_s=wall_time, 
            parsed=parsed
        )

    call_started_at = time.perf_counter()
    raw = _client.chat.completions.create(**payload)
    latency = time.perf_counter() - call_started_at

    choice = raw.choices[0].message
    text = choice.content or ""

    parsed = None

    if response_format is not None:
        parsed = response_format.model_validate_json(text)

    data = {
        "text": text,
        "prompt_tokens": raw.usage.prompt_tokens,
        "completion_tokens": raw.usage.completion_tokens,
        "latency_s": round(latency, 2),
        "model": model,
        "tool_calls": [tc.model_dump() for tc in (choice.tool_calls or [])],
    }

    _cache_write(key, data)

    wall_time = round(time.perf_counter() - started_at, 4)
    logger.info(json.dumps({
        "event": "llm_call",
        "cached": False,
        "model": model,
        "prompt_tokens": data["prompt_tokens"],
        "completion_tokens": data["completion_tokens"],
        "latency_s": data["latency_s"],
        "wall_time_s": wall_time,
        "tok_per_s": round(data["completion_tokens"] / latency ,1) if latency else 0,
    }))
    return LLMResponse(
        **data, 
        wall_time_s=wall_time, 
        parsed=parsed
    )