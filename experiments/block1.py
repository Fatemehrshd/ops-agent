from src.ops_agent.llm import chat
import json
import time

success_count = 0

system_prompt = """You are a shopping assistant for a store.

Respond with JSON only. No explanation, no markdown.

Always respond in the same language as the user's latest message."""
messages = [
    "چند محصول در انبار در حال تمام شدن هستند؟",
    "کدام محصولات تخفیف خورده اند؟",
    "چه محصولات الکترونیکی در فروشگاه موجود است؟",
    "کدام محصول بیشترین فروش در یک ماه گذشته را داشته؟",
    "کدام دسته بندی محصول در ماه گذشته از همه بیشتر تخفیف خورده؟",
    "فردا هوا چطوره؟",
    "پایتخت ژاپن کجاست؟",
    "امروز فروش چطور بود؟",
    "محصولات انبار باید شارژ بشن؟",
    "موجودی شلوار جین آبی آسمانی سایز 34 رو 5 تا اضافه کن."
]

start = time.perf_counter()

for i, user_message in enumerate(messages, 1):
    response = chat([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ])

    raw_output = response.text

    print(f"\n--- Test {i} ---")
    print(f"Input: {user_message}")
    print(f"Raw Output: {raw_output}")

    try:
        parsed = json.loads(raw_output)
        success_count += 1
        print("JSON parsed: SUCCESS")
    except json.JSONDecodeError as e:
        print(f"JSON parse: FAILED - {e}")


duration = time.perf_counter() - start

print(f"\nResult: {success_count} / {len(messages)}")
print(f"{len(messages)} cases took {duration:.2f}s")