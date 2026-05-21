from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class OrderItem(BaseModel):
    sku: str
    quantity: int = Field(gt=0, le=50)


class QuoteRequest(BaseModel):
    customer_id: str
    items: list[OrderItem] = Field(min_length=1)
    destination_zip: str = Field(min_length=5)

    @field_validator("customer_id")
    @classmethod
    def customer_must_be_scoped(cls, value: str) -> str:
        if not value.startswith("cust_"):
            raise ValueError("customer_id must use cust_ contract")
        return value


class QuoteResponse(BaseModel):
    quote_id: str
    subtotal: Decimal
    tax: Decimal
    shipping: Decimal
    total: Decimal
    warnings: list[str] = []


class CheckoutRequest(QuoteRequest):
    payment_token: str = Field(min_length=8)


class CheckoutResponse(BaseModel):
    order_id: str
    status: Literal["accepted"]
    quote: QuoteResponse
    partner_calls: list[str]


class ToolInvocation(BaseModel):
    name: Literal["commerce.quote"]
    arguments: dict[str, Any]

