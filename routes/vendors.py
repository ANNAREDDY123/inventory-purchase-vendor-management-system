from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal

from models.vendor import Vendor

from schemas.vendor import VendorCreate

from services.purchase_service import valid_phone

router = APIRouter(
    prefix="/vendors",
    tags=["Vendors"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Vendor).filter(
        Vendor.email == vendor.email
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Vendor email already exists."
        )

    if not valid_phone(vendor.phone):

        raise HTTPException(
            status_code=400,
            detail="Phone number must contain exactly 10 digits."
        )

    new_vendor = Vendor(
        vendor_name=vendor.vendor_name,
        email=vendor.email,
        phone=vendor.phone,
        address=vendor.address
    )

    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)

    return new_vendor


@router.get("/")
def get_vendors(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Vendor).filter(
        Vendor.is_active == True
    )

    total = query.count()

    vendors = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": vendors
    }


@router.get("/{vendor_id}")
def get_vendor(
    vendor_id: int,
    db: Session = Depends(get_db)
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id,
        Vendor.is_active == True
    ).first()

    if not vendor:

        raise HTTPException(
            status_code=404,
            detail="Vendor not found."
        )

    return vendor


@router.put("/{vendor_id}")
def update_vendor(
    vendor_id: int,
    vendor: VendorCreate,
    db: Session = Depends(get_db)
):

    db_vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id,
        Vendor.is_active == True
    ).first()

    if not db_vendor:

        raise HTTPException(
            status_code=404,
            detail="Vendor not found."
        )

    db_vendor.vendor_name = vendor.vendor_name
    db_vendor.email = vendor.email
    db_vendor.phone = vendor.phone
    db_vendor.address = vendor.address

    db.commit()

    return {
        "message": "Vendor updated successfully."
    }


@router.delete("/{vendor_id}")
def delete_vendor(
    vendor_id: int,
    db: Session = Depends(get_db)
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:

        raise HTTPException(
            status_code=404,
            detail="Vendor not found."
        )

    vendor.is_active = False

    db.commit()

    return {
        "message": "Vendor deactivated successfully."
    }
