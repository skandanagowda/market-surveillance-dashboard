# 🧠 Market Surveillance Dashboard – Data Engineering MVP for Stock Exchange

A **Data Engineering and Analytics prototype** designed to simulate a **Stock Exchange Market Surveillance System** — similar to what exchanges like **ICE (Intercontinental Exchange)** or **NYSE** use to monitor and detect **trading irregularities, spoofing, and layering patterns**.

This project demonstrates how trade alerts can be ingested, processed, stored, and visualized using a **modern data stack** (Airflow, Docker, Python, PostgreSQL, Metabase).

---

## 🚀 Project Overview

**Objective:**  
To design an **end-to-end data pipeline** that continuously monitors market trades, applies surveillance rules, detects anomalies, and visualizes alerts in real-time.

This **MVP prototype** proves how a stock exchange surveillance workflow can be built using open-source tools.  
It combines **data engineering orchestration (Airflow)**, **data storage (PostgreSQL)**, **alert computation (Python)**, and **visual analytics (Metabase)** — all containerized with **Docker**.

---

## 🧩 Real-World Relevance

In live markets, exchanges must identify manipulation patterns such as:
- **Spoofing:** placing large fake orders to mislead prices  
- **Quote Stuffing:** flooding the market with rapid-fire orders  
- **Momentum Ignition:** triggering short-term price movements  
- **Wide Spread Violations:** abnormally large bid-ask spreads  

This project models those detection mechanisms using mock data —  
showing how they can be **automated, tracked, and visualized**.

---

## ⚙️ Tech Stack

| Tool / Service | Purpose |
|----------------|----------|
| 🐍 **Python** | Cleanses raw market data and computes rule-based alerts |
| 🪶 **Apache Airflow** | Orchestrates ETL jobs for data ingestion and rule execution |
| 🐘 **PostgreSQL** | Stores structured alert data and trade metrics |
| 🐳 **Docker** | Containerizes Airflow, PostgreSQL, and Metabase for portability |
| 📊 **Metabase** | Builds an interactive Market Surveillance dashboard |

---

## 🧱 Architecture

```text
         ┌────────────────────────┐
         │     Market Trades      │
         │  (raw CSV / stream)    │
         └──────────┬─────────────┘
                    │
            [ETL Pipeline - Airflow]
                    │
                    ▼
         ┌────────────────────────┐
         │  Python Processing     │
         │  - Apply surveillance  │
         │    rules (spoofing etc)│
         └──────────┬─────────────┘
                    │
                    ▼
         ┌────────────────────────┐
         │   PostgreSQL Database  │
         │  (alerts, metadata)    │
         └──────────┬─────────────┘
                    │
                    ▼
         ┌────────────────────────┐
         │  Metabase Dashboard    │
         │  (visual analytics)    │
         └────────────────────────┘
---

## 📊 Dashboard Overview (Metabase)

The **Market Surveillance Dashboard** aggregates trade anomalies into visually rich insights.

### 📈 Total Alerts and Symbols
Shows the total number of alerts generated and unique instruments affected.

![Dashboard Overview](./screenshots/dashboard.png)

---

### ⏰ Alerts Over Time (Hourly)
Visualizes hourly alert trends to detect active trading periods or manipulation bursts.

![Alerts Over Time (Hourly)](./screenshots/AlertOverTimeHours.png)

---

### ⏱ Alerts Over Time (Minutes)
Provides minute-level granularity for short-term anomaly spikes.

![Alerts Over Time (Minutes)](./screenshots/AlertOverTimeMins.png)

---

### ⚙️ Alert Counts by Rule
Breakdown of alerts by rule type (spoofing, layering, quote stuffing, etc.)

![Alert Counts by Rule](./screenshots/AlertCountsByRules.png)

---

### 🔥 Rule vs Severity Heatmap
Color-coded heatmap showing alert frequency and severity across all surveillance rules.

![Rule vs Severity Heatmap](./screenshots/heatmap.png)

---

## 🧠 How It Works

1. **Data Ingestion (Airflow):**  
   - Airflow DAGs simulate continuous trade data ingestion from CSV or APIs.  
   - Cleans timestamps, normalizes symbol names, and formats order types.

2. **Data Transformation (Python):**  
   - Applies surveillance detection logic for spoofing, layering, quote-stuffing, etc.  
   - Generates alert tables with fields like:
     ```sql
     symbol | timestamp | rule | severity | side | alert_id
     ```

3. **Storage (PostgreSQL):**  
   - Stores structured alerts for querying and trend analysis.  
   - Indexed by rule type and symbol for efficient aggregation.

4. **Visualization (Metabase):**  
   - Connects directly to PostgreSQL using JDBC.  
   - Interactive dashboards with filters (date range, rule type, severity).  
   - Enables compliance officers to view anomalies and take corrective action.

---

## 💻 Local Setup (Docker)

1️⃣ **Clone the repository**
```bash
git clone https://github.com/<your-username>/market-surveillance-dashboard.git
cd market-surveillance-dashboard
