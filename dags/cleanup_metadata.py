from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'admin',
    'depends_on_past': False, 
    'email': ['mjwoo001@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 매일 실행해서 30일 이전의 메타데이터 제거 

with DAG(
    'cleanup_metadata',
    default_args=default_args,
    description='Airflow DAG that removes Airflow Metadata periodically',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 6, 16),
    catchup=False,
) as dag: 
    cleanup_task = BashOperator(
        task_id='cleanup_db',
        bash_command='airflow db cleanup --keep-last 30'
    )