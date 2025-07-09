from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from airflow.providers.mysql.hooks.mysql import MySqlHook
import pandas as pd
from datetime import datetime

def load_customers_to_mysql():
    df = pd.read_csv('/opt/airflow/dags/data/cleaned_customers.csv')

    hook = MySqlHook(mysql_conn_id='mysql_conn')
    rows = df.values.tolist()

    hook.insert_rows(table='customers', rows=rows)

default_args = {'start_date': datetime(2025, 1, 1)}

with DAG(dag_id='load_customers_dag',
         default_args=default_args,
         schedule_interval=None,
         catchup=False) as dag:

    load_task = PythonOperator(
        task_id='load_customers',
        python_callable=load_customers_to_mysql
    )
