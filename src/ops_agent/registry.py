from .tools import (
            get_low_stock,
            get_sales_summary,
            get_discount_query,
            update_stock,
        )

TOOL_REGISTRY = {
    "get_low_stock": get_low_stock,
    "get_sales_summary": get_sales_summary,
    "get_discount_products": get_discount_query,
    "update_stock": update_stock,
}