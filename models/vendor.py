from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean
)

from database import Base


class Vendor(Base):

    __tablename__ = "vendors"

    id = Column(
        Integer,
        primary_key=True
    )

    vendor_name = Column(String)

    email = Column(
        String,
        unique=True
    )

    phone = Column(String)

    address = Column(String)

    is_active = Column(
        Boolean,
        default=True
    )
