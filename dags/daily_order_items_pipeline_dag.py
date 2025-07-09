from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook
from datetime import datetime, timedelta
import pandas as pd
import os
import numpy as np

def get_file_name(execution_date):
    date_str = execution_date.strftime('%Y-%m-%d')
    return f"/opt/airflow/dags/data/order_items_{date_str}.csv"

def wait_for_file(**context):
    file_path = get_file_name(context['execution_date'])
    print(f"Looking for file: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

def process_daily_order_items(**context):
    file_path = get_file_name(context['execution_date'])
    df = pd.read_csv(file_path)

    df['total_price'] = df['price'] + df['shipping_charges']
    df = df.fillna(0)

    hook = MySqlHook(mysql_conn_id='mysql_conn')
    rows = df.values.tolist()

    hook.insert_rows(table='order_items', rows=rows)

default_args = {
    'start_date': datetime(2025, 7, 6),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='daily_order_items_ingestion_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Daily ingestion of order_items files',
    tags=['ecommerce', 'daily_ingestion']
) as dag:

    wait_task = PythonOperator(
        task_id='wait_for_order_items_file',
        python_callable=wait_for_file,
        provide_context=True
    )

    process_task = PythonOperator(
        task_id='process_daily_order_items',
        python_callable=process_daily_order_items,
        provide_context=True
    )

    wait_task >> process_task
