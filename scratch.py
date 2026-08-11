import httpx

def tokens_in(text: str) -> int:
    r = httpx.post(
        "http://localhost:11434/v1/chat/completions",
        json={
            "model": "qwen2.5:7b-instruct",
            "messages": [{"role": "user", "content": text}],
            "max_tokens": 1,
        },
        timeout=120,
    )
    return r.json()["usage"]["prompt_tokens"]

en = "The customer placed an order for three wireless headphones last Tuesday."
fa = "مشتری سه‌شنبهٔ گذشته سفارش سه هدفون بی‌سیم ثبت کرد."

print("EN:", tokens_in(en))
print("FA:", tokens_in(fa))