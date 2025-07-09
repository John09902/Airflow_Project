from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from airflow.providers.mysql.hooks.mysql import MySqlHook
import pandas as pd
import numpy as np
from datetime import datetime

def load_orders_to_mysql():
    df = pd.read_csv('/opt/airflow/dags/data/cleaned_orders.csv')

    # Replace all NaN with None so MySQL accepts them
    df = df.replace({np.nan: None})

    # Convert to list of tuples without NaN
    rows = list(df.itertuples(index=False, name=None))

    # Insert into MySQL
    hook = MySqlHook(mysql_conn_id='mysql_conn')
    hook.insert_rows(table='orders', rows=rows)
default_args = {'start_date': datetime(2025, 1, 1)}

with DAG(dag_id='load_orders_dag',
         default_args=default_args,
         schedule_interval=None,
         catchup=False) as dag:

    load_task = PythonOperator(
        task_id='load_orders',
        python_callable=load_orders_to_mysql
    )
