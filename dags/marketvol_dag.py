from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import os

# 1. Default Arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1), # Adjust to your current date
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# 2. DAG Definition
dag = DAG(
    'marketvol',
    default_args=default_args,
    description='Market Volume Analysis Project',
    schedule='0 18 * * 1-5', # This is the modern keyword
    catchup=False
)

# 3. Python Function for Downloading Data
def download_stock_data(symbol, ds):
    # ds is the execution date provided by Airflow (YYYY-MM-DD)
    start_date = ds
    end_date = (datetime.strptime(ds, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
    
    df = yf.download(symbol, start=start_date, end=end_date, interval='1m')
    
    # Create local filename
    file_path = f"/tmp/{symbol}_raw.csv"
    df.to_csv(file_path, header=True)
    print(f"Downloaded {symbol} data to {file_path}")

# 4. Tasks
# t0: Create directory named after execution date
t0 = BashOperator(
    task_id='tmp_dir_creation',
    bash_command='mkdir -p /tmp/data/{{ ds }}',
    dag=dag,
)

# t1 & t2: Download data
t1 = PythonOperator(
    task_id='download_AAPL',
    python_callable=download_stock_data,
    op_kwargs={'symbol': 'AAPL'},
    dag=dag,
)

t2 = PythonOperator(
    task_id='download_TSLA',
    python_callable=download_stock_data,
    op_kwargs={'symbol': 'TSLA'},
    dag=dag,
)

# t3 & t4: Move files to the dated directory
t3 = BashOperator(
    task_id='move_AAPL',
    bash_command='mv /tmp/AAPL_raw.csv /tmp/data/{{ ds }}/AAPL.csv',
    dag=dag,
)

t4 = BashOperator(
    task_id='move_TSLA',
    bash_command='mv /tmp/TSLA_raw.csv /tmp/data/{{ ds }}/TSLA.csv',
    dag=dag,
)

# t5: Final Query (Simple Python check to see if files exist)
def run_final_query(ds):
    path = f"/tmp/data/{ds}/"
    aapl = pd.read_csv(os.path.join(path, 'AAPL.csv'))
    tsla = pd.read_csv(os.path.join(path, 'TSLA.csv'))
    print(f"Analysis complete for {ds}. AAPL rows: {len(aapl)}, TSLA rows: {len(tsla)}")

t5 = PythonOperator(
    task_id='run_query',
    python_callable=run_final_query,
    dag=dag,
)

# 5. Dependencies
t0 >> [t1, t2]
t1 >> t3
t2 >> t4
[t3, t4] >> t5