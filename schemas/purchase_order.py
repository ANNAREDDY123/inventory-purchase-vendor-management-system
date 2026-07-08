from pydantic import (
    BaseModel,
    Field
)

from datetime import date


class PurchaseOrderCreate(BaseModel):

    vendor_id: int

    product_name: str = Field(..., min_length=2)

    quantity: int = Field(..., gt=0)

    unit_price: float = Field(..., gt=0)

    expected_delivery_date: date

    status: str
