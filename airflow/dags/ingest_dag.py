"""
ingest_dag.py
Orquestra a ingestão diária da Fake Store API para o Snowflake RAW.
"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="ingest_fakestore",
    default_args=default_args,
    description="Ingestão diária da Fake Store API → Snowflake RAW",
    schedule_interval="0 6 * * *",   # todo dia às 6h
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ingestão", "raw"],
) as dag:

    ingest = BashOperator(
        task_id="run_api_client",
        bash_command="cd /opt/airflow && python ingestion/api_client.py",
    )