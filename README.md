markdown
# Market Volume Airflow Mini-Project

## Project Overview
This project uses Apache Airflow to orchestrate a data pipeline that extracts stock market data for AAPL and TSLA from Yahoo Finance.

## Features
- **Scheduling**: Runs at 6 PM every weekday (Mon-Fri).
- **Parallel Processing**: Downloads AAPL and TSLA data simultaneously.
- **Dynamic Directories**: Creates storage folders based on the execution date (`/tmp/data/YYYY-MM-DD`).
- **Error Handling**: Configured with 2 retries and a 5-minute interval.
- **Executor**: Uses Celery Executor (via Docker).

## How to Run
1. Ensure Docker Desktop is running.
2. Open Git Bash and navigate to the project: `cd /c/Users/T_Hic/airflow-stock-project`
3. Start the environment: `docker compose up -d`
4. Access the Airflow UI at `http://localhost:8080` (Login: airflow/airflow).
5. Unpause the `marketvol` DAG and trigger it.

## How to Verify Results
Run the following command in Git Bash to see the generated CSV files:
`docker compose exec airflow-worker ls -R //tmp/data/`