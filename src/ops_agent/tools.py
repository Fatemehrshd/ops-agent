from src.ops_agent.schemas import SalesSummaryParams

GET_LOW_STOCK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_low_stock",
        "description": (
            "Returns products whose current inventory quantity is at or "
            "below a specified threshold. Use this tool when the user asks "
            "which products have low stock, are running out, need "
            "replenishment, or have insufficient inventory. "
            "Only provide threshold when the user explicitly specifies "
            "a threshold value. If the user does not specify a threshold, "
            "omit threshold entirely. Never invent or assume a default "
            "threshold. "
            "Only provide limit when the user explicitly requests a "
            "specific number of products. If no limit is specified, omit "
            "limit."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "threshold": {
                    "type": "integer",
                    "description": (
                        "Maximum inventory quantity considered low stock. "
                        "Provide this only when the user explicitly "
                        "specifies a threshold. Otherwise omit it."
                    ),
                },
                "limit": {
                    "type": "integer",
                    "description": (
                        "Maximum number of products to return. "
                        "Provide this only when the user explicitly "
                        "requests a specific number of products. "
                        "Otherwise omit it."
                    ),
                },
            },
            "required": [],
            "additionalProperties": False,
        },
    },
}

GET_SALES_SUMMARY_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_sales_summary",
        "description": (
            "Returns information about store sales performance. "
            "Use this tool when the user asks about sales totals, revenue, "
            "units sold, best-selling products, sales performance, or "
            "sales trends."
        ),
        "parameters": SalesSummaryParams.model_json_schema(),
    },
}

GET_DISCOUNT_PRODUCTS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_discount_products",
        "description": (
            "Returns products that currently have discounts or promotions. "
            "Use this tool when the user asks which products are discounted, "
            "which products are on sale, or what discounts or promotions "
            "are currently available."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
}

UPDATE_STOCK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "update_stock",
        "description": (
            "Updates the inventory quantity of a specific product. "
            "Use this tool only when the user explicitly asks to increase "
            "or decrease the stock of a specific product. "
            "The item argument must contain only the product name. "
            "The quantity argument must contain only the number of units "
            "to add or remove. Use a positive value when increasing stock "
            "and a negative value when decreasing stock."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "item": {
                    "type": "string",
                    "description": (
                        "The product name only. Do not include quantity, "
                        "numbers, commands, or surrounding words. "
                        "Preserve the original language and wording."
                    ),
                },
                "quantity": {
                    "type": "integer",
                    "description": (
                        "Number of units to add or remove. "
                        "Use a positive value when increasing stock "
                        "and a negative value when decreasing stock."
                    ),
                },
            },
            "required": ["item", "quantity"],
            "additionalProperties": False,
        },
    },
}


def get_low_stock(
    threshold: int | None = None, 
    limit: int | None = None
) -> list[dict]:

    products = [
        {"name": "شلوار جین آبی", "quantity": 3},
        {"name": "لپ‌تاپ مدل X", "quantity": 7},
        {"name": "هدفون بی‌سیم", "quantity": 2},
    ]

    result = [
        product
        for product in products
        if product["quantity"] <= threshold
    ]

    if limit is not None:
        return result[:limit]
    
    return result


def get_sales_summary(period: str | None = None) -> dict:
    return {
        "period": period,
        "total_sales": 1250000,
        "total_count": 45,
    }

def get_discount_products() -> list[dict]:
    return [
        {"name": "هدفون بی سیم", "discount_percent": 20},
        {"name": "کیبورد مکانیکی", "discount_percent": 15},
    ]

def update_stock(item: str, quantity: int) -> dict:
    return {
        "item": item,
        "quantity_change": quantity,
        "status": "updated",
    }