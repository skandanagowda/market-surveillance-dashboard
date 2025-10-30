import os
from fastapi import FastAPI
import psycopg2, json

DATABASE_URL = os.getenv("DATABASE_URL")
app = FastAPI()

def q(sql, params=None):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(sql, params or [])
    cols = [d[0] for d in cur.description] if cur.description else []
    rows = cur.fetchall() if cur.description else []
    cur.close(); conn.close()
    return [dict(zip(cols,r)) for r in rows]

@app.get("/health")
def health(): return {"ok": True}

@app.get("/bars/{sym}")
def bars(sym: str, limit: int = 100):
    return q("""select * from fact_bars_1m where symbol=%s order by ts desc limit %s""", [sym, limit])

@app.get("/factors/{sym}")
def factors(sym: str, limit: int = 100):
    return q("""select symbol, ts, spread_bp, vol_5m, vol_30m, fair_value
                from fact_factors where symbol=%s order by ts desc limit %s""", [sym, limit])

@app.get("/alerts")
def alerts(sym: str | None = None, since: str | None = None, limit: int = 200):
    base = "select id, symbol, ts, rule, score, details from surveillance_alerts where 1=1"
    params = []
    if sym: base += " and symbol=%s"; params.append(sym)
    if since: base += " and ts >= %s"; params.append(since)
    base += " order by ts desc limit %s"; params.append(limit)
    return q(base, params)
