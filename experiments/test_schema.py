from ctypes import resize
import json
from src.ops_agent.llm import chat
from src.ops_agent.schemas import UserIntent
from pydantic import ValidationError
from src.ops_agent.prompts import intent_prompt


schema = json.dumps(UserIntent.model_json_schema(), indent=2)

system_prompt = intent_prompt()

valid_jsons, valid_schemas, correct_intents = 0, 0, 0

# messages = [
#     "چند محصول در انبار در حال تمام شدن هستند؟",
#     "کدام محصولات تخفیف خورده اند؟",
#     "چه محصولات الکترونیکی در فروشگاه موجود است؟",
#     "کدام محصول بیشترین فروش در یک ماه گذشته را داشته؟",
#     "کدام دسته بندی محصول در ماه گذشته از همه بیشتر تخفیف خورده؟",
#     "فردا هوا چطوره؟",
#     "پایتخت ژاپن کجاست؟",
#     "امروز فروش چطور بود؟",
#     "محصولات انبار باید شارژ بشن؟",
#     "موجودی شلوار جین آبی آسمانی سایز 34 رو 5 تا اضافه کن."
# ]
test_cases = [
    {
        "input": "چند محصول در انبار در حال تمام شدن هستند؟",
        "expected_intent": "low_stock",
    },
    {
        "input": "کدام محصولات تخفیف خورده اند؟",
        "expected_intent": "unknown",
    },
    {
        "input": "چه محصولات الکترونیکی در فروشگاه موجود است؟",
        "expected_intent": "unknown",
    },
    {
        "input": "کدام محصول بیشترین فروش در یک ماه گذشته را داشته؟",
        "expected_intent": "sales_summary",
    },
    {
        "input": "کدام دسته بندی محصول در ماه گذشته از همه بیشتر تخفیف خورده؟",
        "expected_intent": "unknown",
    },
    {
        "input": "فردا هوا چطوره؟",
        "expected_intent": "unknown",
    },
    {
        "input": "پایتخت ژاپن کجاست؟",
        "expected_intent": "unknown",
    },
    {
        "input": "امروز فروش چطور بود؟",
        "expected_intent": "sales_summary",
    },
    {
        "input": "محصولات انبار باید شارژ بشن؟",
        "expected_intent": "unknown",
        "note": "genuinely ambiguous: restock vs charge batteries",
    },
    {
        "input": "موجودی شلوار جین آبی آسمانی سایز 34 رو 5 تا اضافه کن.",
        "expected_intent": "update_stock",
    },
]

for i, test in enumerate(test_cases, 1):
    response = chat([
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": test["input"]}
    ])

    text = response.text
    try: 
        parsed = json.loads(text)
        valid_jsons += 1
        print("JSON: SUCCESS")

    except json.JsonDecoderError as e:
        print(f"JSON: FAILED - {e}")

    try: 
        result = UserIntent.model_validate_json(text)
        valid_schemas += 1
        predicted = result.intent
        expected = test["expected_intent"]
        correct_intents += predicted == expected
        
        print(f"\n--- Test {i} ---")
        print(f"Expected: {expected}")
        print(f"Predicted: {predicted}")
    except ValidationError as e:
        print(f"ERROR: {e}")

    print("-" * 20)

print(f"Valid JSON: {valid_jsons}/{len(test_cases)}")
print(f"Valid schemas: {valid_schemas}/{len(test_cases)}")
print(
    "Intent accuracy: "
    f"{correct_intents}/{len(test_cases)} "
    f"({correct_intents / len(test_cases):.0%})")