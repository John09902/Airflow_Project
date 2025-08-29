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

# Alternative using XCom for passing file path between tasks
#
# def get_file_name_task(**context):
#     execution_date = context['execution_date']
#     date_str = execution_date.strftime('%Y-%m-%d')
#     file_path = f"/opt/airflow/dags/data/order_items_{date_str}.csv"
#     return file_path  # pushed automatically to XCom
#
# def process_file_task(**context):
#     ti = context['ti']  # task instance
#     file_path = ti.xcom_pull(task_ids='get_file_name_task')
#     df = pd.read_csv(file_path)
#     # process dataframe here


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
    # Alternative using FileSensor instead of wait_for_file()
# from airflow.sensors.filesystem import FileSensor
#
# wait_for_file = FileSensor(
#     task_id='wait_for_order_items_file',
#     fs_conn_id='fs_default',  # must be defined in Airflow Connections
#     filepath="order_items_{{ ds }}.csv",  # {{ ds }} gives execution_date in YYYY-MM-DD
#     poke_interval=60,  # check every 60 seconds
#     timeout=3600,      # fail after 1 hour if file not found
# )


    wait_task >> process_task

