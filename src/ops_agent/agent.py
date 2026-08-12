import json

from .prompts import tool_calling_prompt
from .registry import TOOL_REGISTRY
from .llm import LLMResponse, chat
from .tools import (
    GET_LOW_STOCK_SCHEMA,
    GET_SALES_SUMMARY_SCHEMA,
    GET_DISCOUNT_QUERY_SCHEMA,
    UPDATE_STOCK_SCHEMA,
)

TOOLS = [
    GET_LOW_STOCK_SCHEMA,
    GET_SALES_SUMMARY_SCHEMA,
    GET_DISCOUNT_QUERY_SCHEMA,
    UPDATE_STOCK_SCHEMA,
]



def run_agent(user_message: str) -> LLMResponse:

    messages= [
        {"role": "system", "content": tool_calling_prompt()},
        {"role": "user", "content": user_message},
    ]

    while True:
        response = chat(
            messages=messages,
            tools=TOOLS,
        )

        if not response.tool_calls:
            return response

        messages.append({
                "role": "assistant",
                "tool_calls": response.tool_calls,
            })

        for tool_call in response.tool_calls:
            tool_name = tool_call["function"]["name"]
            arguments = json.loads(tool_call["function"]["arguments"])

            tool_function = TOOL_REGISTRY[tool_name]
            result = tool_function(**arguments)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": json.dumps(
                    result, 
                    ensure_ascii=False)
            })