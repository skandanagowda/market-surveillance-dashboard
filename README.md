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
