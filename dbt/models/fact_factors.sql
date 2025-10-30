with q as (
  select
    symbol,
    ts,
    (bid + ask)/2.0 as mid,
    (ask - bid)     as spread
  from stg_quotes
),
f as (
  select
    symbol,
    ts,
    10000 * spread / nullif(mid, 0) as spread_bp,
    -- 5-row rolling volatility on mid
    stddev_samp(mid) over (
      partition by symbol
      order by ts
      rows between 5 preceding and current row
    ) as vol_5m,
    -- 30-row rolling volatility on mid (correct window syntax)
    stddev_samp(mid) over (
      partition by symbol
      order by ts
      rows between 30 preceding and current row
    ) as vol_30m,
    mid as fair_value
  from q
)
select * from f
