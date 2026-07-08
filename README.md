# inventory-purchase-vendor-management-system
FastAPI Inventory Purchase &amp; Vendor Management System with JWT Authentication, Vendor Management, Purchase Order Management, Reports, Search, SQLAlchemy ORM, Pagination, Logging, Docker Support, and Unit Tests.
# Inventory Purchase & Vendor Management System

## Features

- JWT Authentication
- Vendor Management (CRUD)
- Purchase Order Management
- Purchase History Reports
- Search, Filter & Pagination
- SQLAlchemy ORM
- SQLite Database
- Docker Support
- Logging
- Basic Unit Tests

---

## Setup Instructions

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Project

```bash
py -m uvicorn main:app --reload
```

Swagger URL

```
http://127.0.0.1:8000/docs
```

---

## Environment Variables

```
SECRET_KEY=inventory_secret_key
ALGORITHM=HS256
```

---

## API Examples

- POST `/auth/register`
- POST `/auth/login`
- POST `/vendors`
- POST `/purchase-orders`

---

## Docker Deployment

```bash
docker build -t inventory-system .
docker run -p 8000:8000 inventory-system
```

---

## Assumptions

- Vendor email must be unique.
- Inactive vendors cannot receive new purchase orders.
- Total amount is calculated automatically.
- Purchase orders with **Received** status cannot be edited.
- Vendor records use soft delete.
