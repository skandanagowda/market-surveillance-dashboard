from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, date
import csv, psycopg2, os, json

DB_URL = "dbname=airflow user=airflow password=airflow host=postgres"

def sql_exec(sql):
    conn = psycopg2.connect(DB_URL); cur = conn.cursor()
    cur.execute(sql); conn.commit(); cur.close(); conn.close()

def bootstrap():
    sql_exec("""
      CREATE TABLE IF NOT EXISTS stg_trades(
        symbol text, ts timestamptz, price numeric, size int
      );
      CREATE TABLE IF NOT EXISTS stg_quotes(
        symbol text, ts timestamptz, bid numeric, ask numeric, bid_size int, ask_size int
      );
      CREATE TABLE IF NOT EXISTS surveillance_alerts(
        id bigserial primary key,
        symbol text, ts timestamptz, rule text, score numeric, details jsonb
      );
      TRUNCATE stg_trades, stg_quotes RESTART IDENTITY;
    """)

def load_csv(table, path, columns):
    conn = psycopg2.connect(DB_URL); cur = conn.cursor()
    with open(path) as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            vals = [r[c] for c in columns]
            cur.execute(
                f"INSERT INTO {table}({','.join(columns)}) VALUES ({','.join(['%s']*len(columns))})",
                vals
            )
    conn.commit(); cur.close(); conn.close()

def load_trades(): load_csv("stg_trades", "/data/raw/trades.csv", ["symbol","ts","price","size"])
def load_quotes(): load_csv("stg_quotes", "/data/raw/quotes.csv", ["symbol","ts","bid","ask","bid_size","ask_size"])

def run_rules():
    conn = psycopg2.connect(DB_URL); cur = conn.cursor()

    # Wide spread (>10 bps)
    cur.execute("""
      insert into surveillance_alerts(symbol, ts, rule, score, details)
      select f.symbol, f.ts, 'wide_spread', spread_bp,
             jsonb_build_object('spread_bp', spread_bp)
      from fact_factors f
      where spread_bp > 0.9;
    """)

    # Return spike (abs(z) > 3) on 1-min returns
    cur.execute("""
      with r as (
        select symbol, ts, (close - lag(close) over (partition by symbol order by ts))
               / nullif(lag(close) over (partition by symbol order by ts),0) as ret
        from fact_bars_1m
      ),
      z as (
        select symbol, ts, ret,
               (ret - avg(ret) over (partition by symbol rows between 10 preceding and current row))
               / nullif(stddev_samp(ret) over (partition by symbol rows between 10 preceding and current row),0) as z
        from r
      )
      insert into surveillance_alerts(symbol, ts, rule, score, details)
      select symbol, ts, 'return_spike', abs(z), jsonb_build_object('ret', ret, 'z', z)
      from z where abs(z) > 3;
    """)
    conn.commit(); cur.close(); conn.close()

def write_daily_csv():
    import csv
    conn = psycopg2.connect(DB_URL); cur = conn.cursor()
    cur.execute("""
      select symbol, ts, rule, score, details
      from surveillance_alerts
      where ts::date = current_date
      order by score desc
    """)
    rows = cur.fetchall()
    os.makedirs("/data/reports", exist_ok=True)
    out = f"/data/reports/alerts_{date.today().isoformat()}.csv"
    with open(out,"w",newline="") as f:
        w=csv.writer(f); w.writerow(["symbol","ts","rule","score","details"])
        for r in rows: w.writerow([r[0], r[1], r[2], r[3], json.dumps(r[4])])
    cur.close(); conn.close()

with DAG(
    "market_surveillance_mvp",
    start_date=datetime(2025,1,1),
    schedule=None,
    catchup=False,
    tags=["mvp"]
) as dag:

    t_bootstrap = PythonOperator(task_id="bootstrap", python_callable=bootstrap)
    t_load_trades = PythonOperator(task_id="load_trades", python_callable=load_trades)
    t_load_quotes = PythonOperator(task_id="load_quotes", python_callable=load_quotes)

    t_dbt = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/dbt && dbt run --profiles-dir /opt/dbt"
    )

    t_rules = PythonOperator(task_id="run_rules", python_callable=run_rules)
    t_report = PythonOperator(task_id="write_daily_csv", python_callable=write_daily_csv)

    t_bootstrap >> [t_load_trades, t_load_quotes] >> t_dbt >> t_rules >> t_report
