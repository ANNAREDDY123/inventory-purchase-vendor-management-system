import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from routes.auth import router as auth_router
from routes.vendors import router as vendors_router
from routes.purchase_orders import router as purchase_orders_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory Purchase & Vendor Management System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(vendors_router)
app.include_router(purchase_orders_router)


@app.get("/")
def home():

    logger.info("Application Started Successfully")

    return {
        "message": "Inventory Purchase & Vendor Management System"
    }
