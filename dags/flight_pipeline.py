from datetime import datetime ,timedelta
from airflow import DAG
import sys
from pathlib import Path
from airflow.operators.python import PythonOperator
import warnings
warnings.filterwarnings(
    "ignore",
    message="This process.*is multi-threaded, use of fork.*may lead to deadlocks",
    category=DeprecationWarning
)

AIRFLOW_HOME = Path("/opt/airflow")

if str(AIRFLOW_HOME) not in sys.path:
    sys.path.insert(0,str(AIRFLOW_HOME))

from scripts.bronze_ingested import run_bronze_ingestion
from scripts.sliver_transform import run_silver_transform
from scripts.gold_aggregation import run_gold_aggregate
from scripts.load_gold_to_snowflake import load_gold_to_snowflake
default_args = {
    "owner":"airflow",
    "retries": 0,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id = "flights_ops_medallions_pipeline",
    default_args= default_args,
    start_date = datetime(2026,2,9),
    schedule_interval = "*/5 * * * *",
    catchup  = False,
    tags = ["flight"]
) as dag:
    bronze = PythonOperator(
        task_id = "bronze_ingest",
        python_callable = run_bronze_ingestion
    )
    silver = PythonOperator(
        task_id = "sliver_transform",
        python_callable = run_silver_transform
    )
    gold = PythonOperator(
        task_id = "gold_agg",
        python_callable = run_gold_aggregate
    )
    load_to_snowflake = PythonOperator(
        task_id = "load_tosnowflake",
        python_callable = load_gold_to_snowflake
    )

    bronze >> silver >> gold >> load_to_snowflake