create database project;
use project;
-- Loading Data from DAG into these Tables
-- customers
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    zip_code_prefix INT,
    city VARCHAR(100),
    state VARCHAR(5)
);

-- orders
CREATE TABLE orders (
  order_id VARCHAR(50),
  customer_id VARCHAR(50),
  order_status VARCHAR(20),
  order_purchase_timestamp DATETIME,
  order_approved_at DATETIME,
  order_delivered_timestamp DATETIME,
  order_estimated_delivery_date DATETIME,
  delivery_time_days INT
);

-- order_items
CREATE TABLE IF NOT EXISTS order_items (
    order_id VARCHAR(50),
    product_id VARCHAR(50),
    seller_id VARCHAR(50),
    price FLOAT,
    shipping_charges FLOAT,
    total_price FLOAT
);

-- payments
CREATE TABLE IF NOT EXISTS payments (
    order_id VARCHAR(50),
    payment_type VARCHAR(50),
    installments INT,
    payment_value FLOAT
);

-- products
CREATE TABLE products (
  product_id VARCHAR(50),
  product_category_name VARCHAR(100),
  product_weight_g FLOAT,
  product_length_cm FLOAT,
  product_height_cm FLOAT,
  product_width_cm FLOAT,
  product_volume_cm3 FLOAT
);

-- Gold Table 
CREATE TABLE IF NOT EXISTS daily_sales_summary (
    order_date DATE primary key,
    total_orders INT,
    total_revenue FLOAT,
    avg_order_value FLOAT
);

CREATE TABLE IF NOT EXISTS customer_lifetime_value (
    customer_id VARCHAR(50) primary key,
    total_orders INT,
    total_spent FLOAT,
    avg_order_value FLOAT
);

CREATE TABLE IF NOT EXISTS product_performance (
    product_id VARCHAR(50) primary key,
    total_sold INT,
    total_revenue FLOAT
);
