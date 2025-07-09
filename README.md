# 🛠 Apache Airflow End-to-End ETL Project

This project demonstrates an end-to-end **ETL pipeline using Apache Airflow**, simulating a real-world e-commerce data flow from ingestion to reporting.

---

## 🚀 Tech Stack
- **Apache Airflow** (Dockerized)
- **MySQL** (local + Airflow connection)
- **Python + Pandas** (for data cleaning)
- **SQL** (for aggregation in Gold layer)
- **Jupyter Notebook** (for exploration)
- **Git + GitHub** (for versioning)

---

## 🧱 Project Structure

### Step 1 – Data Collection
- Dataset from Kaggle: *E-commerce Orders & Supply Chain*
- 5 Raw CSVs used: `customers`, `orders`, `order_items`, `payments`, `products`

### Step 2 – Data Cleaning
- Performed in Jupyter using Pandas
- Removed nulls, standardized formats, derived columns like `delivery_days`, `total_price`, `volume`

### Step 3 – Load Cleaned Data to MySQL
- Airflow DAGs created to load all cleaned files:
    - `load_customers_dag.py`
    - `load_orders_dag.py`
    - `load_order_items_dag.py`
    - `load_payments_dag.py`
    - `load_products_dag.py`

### Step 4 – Build Gold Summary Tables (Reporting Layer)
- Aggregated summaries built using `MySqlOperator`:
    - `daily_sales_summary`
    - `customer_lifetime_value`
    - `product_performance`

### Step 5 – Add Daily Incremental Load
- Simulated daily `order_items` CSV
- File sensor detects new files
- DAG loads the new rows into MySQL
- Gold Summary tables updated automatically

### Step 6 – Monitoring & Alerts
- Added a notification task at the end of Gold DAG
- Can be extended to send Email/Slack alerts

---

## 📂 Folders
- `/dags` – All Airflow DAGs
- `/data` – Cleaned CSVs + daily file samples
- `/schema` – MySQL table creation scripts
- `/notebooks` – Data exploration & cleaning notebook

---

## 📌 Real-World Concepts Used
- DAG scheduling & task dependencies
- XCom and PythonOperator
- FileSensor
- SQL aggregations with `MySqlOperator`
- Incremental load simulation
- GitHub-hosted project codebase

---

## 🔗 Credits
Dataset: Kaggle – [E-commerce Supply Chain](https://www.kaggle.com/datasets/prachi13/customer-analytics)
