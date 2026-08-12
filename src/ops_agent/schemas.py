from pydantic import BaseModel, Field
from typing import Literal


class UserIntent(BaseModel):
    intent: Literal[
        "low_stock",
        "sales_summary",
        "update_stock",
        "unknown"
    ]
    threshold: int | None = None
    limit: int | None = None
    item: str | None = None         # for stock update
    quantity: int | None = None
    confidence: float = Field(ge=0, le=1)

class SalesSummaryParams(BaseModel):
    period: str = Literal["today", "last_7_days", "last_30_days"]
    