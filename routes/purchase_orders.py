from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal

from models.purchase_order import PurchaseOrder
from models.vendor import Vendor

from schemas.purchase_order import PurchaseOrderCreate

from services.purchase_service import (
    valid_status,
    calculate_total
)

router = APIRouter(
    prefix="/purchase-orders",
    tags=["Purchase Orders"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_purchase_order(
    order: PurchaseOrderCreate,
    db: Session = Depends(get_db)
):

    vendor = db.query(Vendor).filter(
        Vendor.id == order.vendor_id,
        Vendor.is_active == True
    ).first()

    if not vendor:

        raise HTTPException(
            status_code=404,
            detail="Vendor not found or inactive."
        )

    if not valid_status(order.status):

        raise HTTPException(
            status_code=400,
            detail="Invalid purchase order status."
        )

    total = calculate_total(
        order.quantity,
        order.unit_price
    )

    new_order = PurchaseOrder(
        vendor_id=order.vendor_id,
        product_name=order.product_name,
        quantity=order.quantity,
        unit_price=order.unit_price,
        total_amount=total,
        expected_delivery_date=order.expected_delivery_date,
        status=order.status
    )

    db.add(new_order)

    db.commit()

    db.refresh(new_order)

    return new_order


@router.get("/")
def get_purchase_orders(
    vendor_id: int = None,
    product_name: str = None,
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(PurchaseOrder)

    if vendor_id:
        query = query.filter(
            PurchaseOrder.vendor_id == vendor_id
        )

    if product_name:
        query = query.filter(
            PurchaseOrder.product_name.contains(product_name)
        )

    if status:
        query = query.filter(
            PurchaseOrder.status == status
        )

    total = query.count()

    orders = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": orders
    }


@router.get("/{order_id}")
def get_purchase_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(PurchaseOrder).filter(
        PurchaseOrder.id == order_id
    ).first()

    if not order:

        raise HTTPException(
            status_code=404,
            detail="Purchase order not found."
        )

    return order


@router.put("/{order_id}")
def update_purchase_order(
    order_id: int,
    order: PurchaseOrderCreate,
    db: Session = Depends(get_db)
):

    db_order = db.query(PurchaseOrder).filter(
        PurchaseOrder.id == order_id
    ).first()

    if not db_order:

        raise HTTPException(
            status_code=404,
            detail="Purchase order not found."
        )

    if db_order.status == "Received":

        raise HTTPException(
            status_code=400,
            detail="Received purchase orders cannot be edited."
        )

    db_order.vendor_id = order.vendor_id
    db_order.product_name = order.product_name
    db_order.quantity = order.quantity
    db_order.unit_price = order.unit_price
    db_order.total_amount = calculate_total(
        order.quantity,
        order.unit_price
    )
    db_order.expected_delivery_date = order.expected_delivery_date
    db_order.status = order.status

    db.commit()

    return {
        "message": "Purchase order updated successfully."
    }


@router.get("/vendor/{vendor_id}")
def vendor_purchase_history(
    vendor_id: int,
    db: Session = Depends(get_db)
):

    return db.query(PurchaseOrder).filter(
        PurchaseOrder.vendor_id == vendor_id
    ).all()
