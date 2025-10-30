FROM apache/airflow:2.9.2
USER root
RUN apt-get update && apt-get install -y --no-install-recommends build-essential git \
    && rm -rf /var/lib/apt/lists/*
USER airflow
# install dbt for Postgres inside the Airflow image
RUN pip install --no-cache-dir "dbt-postgres==1.8.*" psycopg2-binary