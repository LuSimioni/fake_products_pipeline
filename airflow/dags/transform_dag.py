
"""
transform_dag.py
Orquestra: Spark (Bronze→Silver) depois dbt (Silver→Gold).
Roda após a ingestão.
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
    dag_id="transform_pipeline",
    default_args=default_args,
    description="Spark Bronze→Silver + dbt Silver→Gold",
    schedule_interval="0 7 * * *",   # 1h depois da ingestão
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["spark", "dbt", "transform"],
) as dag:

    spark_job = BashOperator(
        task_id="run_spark_bronze_to_silver",
        bash_command="cd /opt/airflow && python spark/jobs/bronze_to_silver.py",
    )

    dbt_run = BashOperator(
        task_id="run_dbt",
        bash_command="cd /opt/airflow/dbt && dbt run --profiles-dir .",
    )

    dbt_test = BashOperator(
        task_id="run_dbt_tests",
        bash_command="cd /opt/airflow/dbt && dbt test --profiles-dir .",
    )

    spark_job >> dbt_run >> dbt_test