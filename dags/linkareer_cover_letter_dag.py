from airflow import DAG
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from datetime import datetime, date, timezone, timedelta
from logger import setup_logger
from preprocess import csv_to_vectorDB
from scraper import LinkareerCoverLetterScraper
import os 

default_args = {
    'start_date': datetime(2024, 6, 28), 
    'email_on_failure': False, 
    'email_on_retry': False,
}

dag = DAG(
    dag_id="linkareer_cover_letter_dag",
    default_args=default_args,
    description='Scrape Linkareer cover letters and preprocess the data',
    schedule_interval="@daily"
)

def scrape_linkareer_cover_letters(): 
    log = setup_logger()
    Linkareer_crawler = LinkareerCoverLetterScraper(log=log, background=True)
        
    try:
        Linkareer_crawler.open_website("https://linkareer.com/cover-letter/search")
        Linkareer_crawler.scrape_data()
    except Exception as e:
        log.error(f"An error occurred: {str(e)}")
    finally:
        Linkareer_crawler.convert_to_DataFrame()
        Linkareer_crawler.sort_columns_for_RAG()
        Linkareer_crawler.save_to_csv("./data/Linkareer_Cover_Letter_Data.csv")
        Linkareer_crawler.close_browser()
    
# vectorize the data 
def preprocess_data():
    csv_to_vectorDB("./data/Linkareer_Cover_Letter_Data.csv")

# upload data to S3 bucket 
# S3 file directory format : daily/yyyymmdd/filename.csv
def upload_to_s3(filename: str, bucket_name: str) -> None:
    hook = S3Hook('aws_default')
    file_obj = filename.split('/')[-1]
    KST = timezone(timedelta(hours=9))
    time_record = datetime.now(KST).strftime("%Y%m%d")
   
    key = "daily/"+ time_record + "/" + file_obj
    hook.load_file(filename=filename, key=key, bucket_name=bucket_name)

scrape_task = PythonOperator(
    task_id='scrape_linkareer_cover_letters_task',
    python_callable=scrape_linkareer_cover_letters,
    dag=dag,
)

preprocess_task = PythonOperator(
    task_id='preprocess_data_task',
    python_callable=preprocess_data,
    dag=dag,
)

upload_task = PythonOperator(
    task_id='upload_to_s3',
    python_callable=upload_to_s3,
    op_kwargs = {
        'filename' : './data/Linkareer_Cover_Letter_Data.csv',
        'bucket_name': 'resumait-data'
    },
    dag=dag,
)

scrape_task >> preprocess_task >> upload_task