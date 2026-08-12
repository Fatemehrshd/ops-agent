from src.ops_agent.llm import chat
from src.ops_agent.tools import (
    GET_LOW_STOCK_SCHEMA,
    GET_SALES_SUMMARY_SCHEMA,
    GET_DISCOUNT_QUERY_SCHEMA,
    UPDATE_STOCK_SCHEMA,
)
from src.ops_agent.prompts import tool_calling_prompt
import json


TOOLS = [
    GET_LOW_STOCK_SCHEMA,
    GET_SALES_SUMMARY_SCHEMA,
    GET_DISCOUNT_QUERY_SCHEMA,
    UPDATE_STOCK_SCHEMA,
]


test_cases = [
    # -------------------------
    # get_low_stock
    # -------------------------
    {
        "input": "کدام محصولات موجودی کمی دارند؟",
        "expected_tool": "get_low_stock",
        "expected_arguments": {},
    },
    {
        "input": "چه محصولاتی دارن تموم میشن؟",
        "expected_tool": "get_low_stock",
        "expected_arguments": {},
    },
    {
        "input": "محصولاتی که موجودی‌شان کمتر از ۵ تاست را نشان بده.",
        "expected_tool": "get_low_stock",
        "expected_arguments": {
            "threshold": 5,
        },
    },
    {
        "input": "۱۰ محصولی که نیاز به شارژ موجودی دارند را نشان بده.",
        "expected_tool": "get_low_stock",
        "expected_arguments": {
            "limit": 10,
        },
    },

    # -------------------------
    # get_sales_summary
    # -------------------------
    {
        "input": "فروش امروز چطور بوده؟",
        "expected_tool": "get_sales_summary",
        "expected_arguments": {},
    },
    {
        "input": "پرفروش‌ترین محصول این ماه کدام بوده؟",
        "expected_tool": "get_sales_summary",
        "expected_arguments": {},
    },
    {
        "input": "میزان فروش هفته گذشته چقدر بوده؟",
        "expected_tool": "get_sales_summary",
        "expected_arguments": {},
    },
    {
        "input": "فروش محصولات در ماه گذشته چه روندی داشته؟",
        "expected_tool": "get_sales_summary",
        "expected_arguments": {},
    },

    # -------------------------
    # get_discount_query
    # -------------------------
    {
        "input": "کدام محصولات تخفیف دارند؟",
        "expected_tool": "get_discount_query",
        "expected_arguments": {},
    },
    {
        "input": "چه محصولاتی الان حراج هستند؟",
        "expected_tool": "get_discount_query",
        "expected_arguments": {},
    },
    {
        "input": "محصولات دارای تخفیف را نشان بده.",
        "expected_tool": "get_discount_query",
        "expected_arguments": {},
    },
    {
        "input": "بیشترین تخفیف مربوط به کدام محصولات است؟",
        "expected_tool": "get_discount_query",
        "expected_arguments": {},
    },

    # -------------------------
    # update_stock
    # -------------------------
    {
        "input": "۵ تا شلوار جین آبی به موجودی اضافه کن.",
        "expected_tool": "update_stock",
        "expected_arguments": {
            "item": "شلوار جین آبی",
            "quantity": 5,
        },
    },
    {
        "input": "موجودی لپ‌تاپ مدل X را ۳ عدد کم کن.",
        "expected_tool": "update_stock",
        "expected_arguments": {
            "item": "لپ‌تاپ مدل X",
            "quantity": -3,
        },
    },

    # -------------------------
    # No tool
    # -------------------------
    {
        "input": "فردا هوا چطوره؟",
        "expected_tool": None,
        "expected_arguments": None,
    },
    {
        "input": "پایتخت ژاپن کجاست؟",
        "expected_tool": None,
        "expected_arguments": None,
    },
]


tool_correct = 0
arguments_correct = 0
fully_correct = 0


for i, test in enumerate(test_cases, 1):

    response = chat(
        [
            {
                "role": "system",
                "content": tool_calling_prompt(),
            },
            {
                "role": "user",
                "content": test["input"],
            },
        ],
        tools=TOOLS,
    )

    tool_calls = response.tool_calls

    # -------------------------
    # No tool expected
    # -------------------------
    if test["expected_tool"] is None:

        predicted_tool = None
        predicted_arguments = None

        if not tool_calls:
            tool_correct += 1
            arguments_correct += 1
            fully_correct += 1

        print(f"\n--- Test {i} ---")
        print(f"Input: {test['input']}")
        print(f"Expected tool: {test['expected_tool']}")
        print(f"Predicted tool: {predicted_tool}")
        print(f"Expected arguments: {test['expected_arguments']}")
        print(f"Predicted arguments: {predicted_arguments}")

        if not tool_calls:
            print("RESULT: PASS")
        else:
            print("RESULT: FAIL")

        continue

    # -------------------------
    # Tool expected
    # -------------------------
    predicted_tool = None
    predicted_arguments = None

    if tool_calls:
        tool_call = tool_calls[0]

        predicted_tool = tool_call["function"]["name"]

        predicted_arguments = json.loads(
            tool_call["function"]["arguments"]
        )

    tool_ok = predicted_tool == test["expected_tool"]
    arguments_ok = predicted_arguments == test["expected_arguments"]

    if tool_ok:
        tool_correct += 1

    if arguments_ok:
        arguments_correct += 1

    if tool_ok and arguments_ok:
        fully_correct += 1

    print(f"\n--- Test {i} ---")

    print(f"Expected tool: {test['expected_tool']}")
    print(f"Predicted tool: {predicted_tool}")

    print(f"Expected arguments: {test['expected_arguments']}")
    print(f"Predicted arguments: {predicted_arguments}")

    print(f"Tool selection: {'PASS' if tool_ok else 'FAIL'}")
    print(f"Arguments: {'PASS' if arguments_ok else 'FAIL'}")
    print(f"Overall: {'PASS' if tool_ok and arguments_ok else 'FAIL'}")


# -------------------------
# Final results
# -------------------------

total = len(test_cases)

print("\n" + "=" * 50)
print("RESULTS")
print("=" * 50)

print(
    f"Tool selection accuracy: "
    f"{tool_correct}/{total} "
    f"({tool_correct / total:.0%})"
)

print(
    f"Argument accuracy: "
    f"{arguments_correct}/{total} "
    f"({arguments_correct / total:.0%})"
)

print(
    f"Fully correct: "
    f"{fully_correct}/{total} "
    f"({fully_correct / total:.0%})"
)