from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2024, 1, 1),
}

with DAG(
    dag_id='gold_summary_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['gold', 'summary'],
) as dag:

    daily_sales_summary = MySqlOperator(
        task_id='daily_sales_summary',
        mysql_conn_id='mysql_conn',
        sql="""
        REPLACE INTO daily_sales_summary
        SELECT
            DATE(order_purchase_timestamp) AS order_date,
            COUNT(DISTINCT o.order_id) AS total_orders,
            SUM(oi.price + oi.shipping_charges) AS total_revenue,
            ROUND(SUM(oi.price + oi.shipping_charges) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY order_date
        ORDER BY order_date;
        """
    )

    customer_ltv = MySqlOperator(
        task_id='customer_lifetime_value',
        mysql_conn_id='mysql_conn',
        sql="""
        REPLACE INTO customer_lifetime_value
        SELECT
            o.customer_id,
            COUNT(DISTINCT o.order_id) AS total_orders,
            SUM(oi.price + oi.shipping_charges) AS total_spent,
            ROUND(SUM(oi.price + oi.shipping_charges) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY o.customer_id;
        """
    )

    product_performance = MySqlOperator(
        task_id='product_performance',
        mysql_conn_id='mysql_conn',
        sql="""
        REPLACE INTO product_performance
        SELECT
            oi.product_id,
            COUNT(*) AS total_sold,
            SUM(oi.price + oi.shipping_charges) AS total_revenue
        FROM order_items oi
        GROUP BY oi.product_id;
        """
    )

def notify_completion():
    print("✅ Gold Layer summary tables created successfully!")

notify_task = PythonOperator(
    task_id='notify_completion',
    python_callable=notify_completion,
    dag=dag,
)
    # Dependency order 
[daily_sales_summary, customer_ltv, product_performance] >> notify_task
