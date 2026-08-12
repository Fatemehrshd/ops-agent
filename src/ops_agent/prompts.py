from .schemas import UserIntent
import json

def intent_prompt() -> str:

    schema = json.dumps(
        UserIntent.model_json_schema(), 
        ensure_ascii=False, 
        indent=2
    )
    prompt = f"""You are an intent classifier for a store assistant.

    Classify the user's latest message into exactly one of the allowed intents defined by the JSON Schema below.

    Return ONLY a valid JSON object that conforms to this schema:
    {schema}

    Rules:
    1. Never answer the user's question. Only classify its intent.
    2. Use only the intent values allowed by the schema.
    3. If the request is outside the store's scope, set "intent" to "unknown".
    4. If the user's intent is unclear or cannot be confidently mapped to an allowed intent, set "intent" to "unknown".
    5. Never guess an intent.
    6. Do not include Markdown, code fences, explanations, comments, or any text outside the JSON object.
    7. Do not invent values for parameters that are not present or implied by the user's request.

    Examples:

    Input: کدام محصولات کم موجود هستند؟
    Output: {{"intent": "low_stock", "threshold": null, "limit": null, "confidence": 0.9}}

    Input: پایتخت ژاپن کجاست؟
    Output: {{"intent": "unknown", "threshold": null, "limit": null, "confidence": 0.95}}
    """
    return prompt