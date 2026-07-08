from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey
)

from database import Base


class PurchaseOrder(Base):

    __tablename__ = "purchase_orders"

    id = Column(
        Integer,
        primary_key=True
    )

    vendor_id = Column(
        Integer,
        ForeignKey("vendors.id")
    )

    product_name = Column(String)

    quantity = Column(Integer)

    unit_price = Column(Float)

    total_amount = Column(Float)

    expected_delivery_date = Column(Date)

    status = Column(
        String,
        default="Pending"
    )
