# GitSentinel — Code Risk Analytics Platform

GitSentinel is a full-stack analytics system that analyzes Git repositories to identify **high-risk files, bug-prone areas, and developer hotspots**. It processes commit history, computes risk metrics, and visualizes insights through an interactive dashboard.


## 🔥 Features

* 📊 **File Risk Analysis** — Detect high-risk files using churn + commit patterns
* 🐞 **Bug Density Tracking** — Identify files with frequent bug-related commits
* 👨‍💻 **Developer Risk Scoring** — Highlight contributors linked to risky changes
* 📈 **Risk Timeline** — Track code churn trends over time
* 🌐 **Live Dashboard** — Interactive charts powered by Chart.js
* ⚡ **Real-time API** — Built with FastAPI

---

## 🧠 How It Works

1. Extract Git history using PyDriller
2. Store commits, files, and changes in PostgreSQL
3. Compute:

   * Code churn
   * Bug density (based on commit messages)
   * Risk score = churn × frequency × bug factor
4. Expose insights via REST APIs
5. Visualize data using a dashboard

---

## 🏗️ Tech Stack

* **Backend:** FastAPI, Python
* **Database:** PostgreSQL (Neon)
* **ORM:** SQLAlchemy
* **Data Extraction:** PyDriller
* **Frontend:** HTML, JavaScript, Chart.js
* **Deployment:** Render

---

## 🌐 Live Demo

👉 https://gitsentinel.onrender.com/dashboard

---

## 📡 API Endpoints

* `/bug-risk` → File risk + bug density
* `/developers` → Developer risk scores
* `/risk-timeline` → Code churn over time
* `/dashboard` → Interactive UI

---

## ⚙️ Setup Instructions

### 1. Clone repo

```bash
git clone https://github.com/your-username/GitSentinel.git
cd GitSentinel
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variable

```bash
export DATABASE_URL=your_postgres_url
```

(Windows PowerShell)

```powershell
$env:DATABASE_URL="your_postgres_url"
```

### 4. Initialize database

```bash
python -m scripts.init_db
```

### 5. Run ingestion

```bash
python -m scripts.ingest_repo
```

### 6. Start server

```bash
uvicorn app.api.main:app --reload
```

---

## 📊 Example Output

```json
[
  {
    "file": "JsonParser.java",
    "risk": 48067.39,
    "bug_density": 0.30
  }
]
```

---

## 🚧 Challenges Solved

* Handling large Git histories efficiently
* Designing scalable database schema
* Debugging environment & deployment issues
* Ensuring consistency between local and cloud DB
* Building a full data pipeline from scratch

---

## 🚀 Future Improvements

* 🔍 File-level drill-down (click → history view)
* 📊 Advanced ML-based risk prediction
* 🌐 Multi-repository support
* 🔐 Authentication & user-based dashboards

---

## 👤 Author

Built by **Anam Saqib**

---

## ⭐ Why This Project Matters

GitSentinel demonstrates:

* Backend system design
* Data engineering pipeline
* Real-world debugging & deployment
* Full-stack integration

---
