
  create view "airflow"."public"."fact_bars_1m__dbt_tmp"
    
    
  as (
    with t as (
  select symbol, date_trunc('minute', ts) as ts_min, ts, price::numeric as price, size::int as size
  from stg_trades
),
open_close as (
  select
    symbol, ts_min,
    first_value(price) over (partition by symbol, ts_min order by ts asc)  as open,
    first_value(price) over (partition by symbol, ts_min order by ts desc) as close
  from t
),
hlv as (
  select symbol, ts_min, min(price) as low, max(price) as high, sum(size) as volume
  from t
  group by symbol, ts_min
)
select
  h.symbol,
  h.ts_min as ts,
  o.open, h.high, h.low, o.close, h.volume
from hlv h
join open_close o using (symbol, ts_min)
order by 1,2
  );