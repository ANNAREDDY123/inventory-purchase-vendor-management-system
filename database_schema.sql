CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50)
);

CREATE TABLE vendors(
    id INTEGER PRIMARY KEY,
    vendor_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    address VARCHAR(255),
    is_active BOOLEAN
);

CREATE TABLE purchase_orders(
    id INTEGER PRIMARY KEY,
    vendor_id INTEGER,
    product_name VARCHAR(100),
    quantity INTEGER,
    unit_price FLOAT,
    total_amount FLOAT,
    expected_delivery_date DATE,
    status VARCHAR(50)
);
