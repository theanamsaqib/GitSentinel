from fastapi import FastAPI
from app.analysis.time_risk import get_risk_over_time
from app.storage.db import SessionLocal
from app.analysis.risk import get_file_risk_scores
from app.analysis.combined_risk import get_combined_risk
from fastapi.responses import HTMLResponse
from sqlalchemy import text
app = FastAPI()


@app.get("/")
def root():
    return {"message": "GitSentinel API running"}


@app.get("/hotspots")
def hotspots():
    session = SessionLocal()
    data = get_file_risk_scores(session)
    session.close()

    return [
        {
            "file": file_path,
            "change_count": int(count),
            "churn": int(churn),
            "risk": float(risk)
        }
        for file_path, count, churn, risk in data
    ]


@app.get("/developers")
def developer_risk():
    session = SessionLocal()
    data = get_combined_risk(session)
    session.close()

    max_score = max(score for _, score in data) if data else 1

    return [
        {
            "name": name,
            "score": round((score / max_score) * 100, 2)
        }
        for name, score in data
    ]
@app.get("/bug-risk")
def bug_risk():
    session = SessionLocal()

    try:
        data = get_file_risk_scores(session)

        if not data:
            return []

        
        cleaned = []
        for file, count, churn, bug_density, risk in data:
            cleaned.append((
                file,
                int(count),
                int(churn),
                float(bug_density),
                float(risk)
            ))

        max_risk = max(r for _, _, _, _, r in cleaned)

        output = []

        for file, count, churn, bug_density, risk in cleaned:

            # normalize
            normalized = (risk / max_risk) * 100

            # priority
            priority = normalized * (1 + bug_density)

            # severity
            if priority > 120:
                severity = "CRITICAL"
            elif priority > 80:
                severity = "HIGH"
            elif priority > 40:
                severity = "MEDIUM"
            else:
                severity = "LOW"

            # explanation
            reasons = []

            if bug_density > 0.3:
                reasons.append("high bug frequency")

            if count > 20:
                reasons.append("frequent changes")

            if churn > 500:
                reasons.append("large code churn")

            output.append({
                "file": file,
                "risk_score": round(normalized, 2),
                "bug_density": round(bug_density, 2),
                "priority_score": round(priority, 2),
                "severity": severity,
                "reason": ", ".join(reasons)
            })

        # sort by priority
        output.sort(key=lambda x: x["priority_score"], reverse=True)

        return output

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}

    finally:
        session.close()
@app.get("/risk-timeline")
def risk_timeline():
    session = SessionLocal()
    data = get_risk_over_time(session)
    session.close()

    return [
        {"month": str(month), "churn": int(churn)}
        for month, churn in data
    ]
@app.get("/file-detail")
def file_detail(file: str):
    session = SessionLocal()

    query = """
    SELECT SUM(lines_added + lines_deleted)
    FROM file_changes fc
    JOIN files f ON fc.file_id = f.id
    WHERE f.file_path = :file
    """

    result = session.execute(text(query), {"file": file}).fetchone()
    session.close()

    return {"file": file, "churn": int(result[0] or 0)}
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return """
<!DOCTYPE html>
<html>
<head>
<title>GitSentinel</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
:root {
    --bg: #0d1117;
    --card: #161b22;
    --border: #30363d;
    --text: #c9d1d9;
    --muted: #8b949e;
    --accent: #58a6ff;
}

body {
    margin: 0;
    font-family: Inter, Arial;
    background: var(--bg);
    color: var(--text);
}

/* Header */
.header {
    padding: 20px;
    border-bottom: 1px solid var(--border);
    font-size: 20px;
    font-weight: 600;
}

/* Layout */
.container {
    padding: 20px;
}

.grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
}

/* Cards */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 15px;
}

.card h3 {
    margin: 0 0 10px 0;
    font-size: 14px;
    color: var(--muted);
}

/* KPI Row */
.kpis {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
}

.kpi {
    background: var(--card);
    padding: 15px;
    border-radius: 10px;
    border: 1px solid var(--border);
    flex: 1;
}

.kpi h4 {
    margin: 0;
    font-size: 12px;
    color: var(--muted);
}

.kpi p {
    margin: 5px 0 0;
    font-size: 18px;
    font-weight: bold;
}

/* Canvas */
canvas {
    width: 100% !important;
    height: 300px !important;
}
</style>
</head>

<body>

<div class="header">GitSentinel Dashboard</div>

<div class="container">

<!-- KPIs -->
<div class="kpis">
    <div class="kpi">
        <h4>Total Files</h4>
        <p id="kpi-files">-</p>
    </div>
    <div class="kpi">
        <h4>Avg Risk</h4>
        <p id="kpi-risk">-</p>
    </div>
    <div class="kpi">
        <h4>High Risk Files</h4>
        <p id="kpi-high">-</p>
    </div>
</div>

<div class="grid">

    <div class="card">
        <h3>File Risk</h3>
        <canvas id="riskChart"></canvas>
    </div>

    <div class="card">
        <h3>Bug Density</h3>
        <canvas id="bugChart"></canvas>
    </div>

    <div class="card">
        <h3>Developer Risk</h3>
        <canvas id="devChart"></canvas>
    </div>

    <div class="card">
        <h3>Risk Over Time</h3>
        <canvas id="timeChart"></canvas>
    </div>

</div>
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {

    let fullData = [];
    let chartInstance = null;

    const searchBox = document.createElement("input");
    searchBox.placeholder = "Search file...";
    searchBox.style = "padding:8px;margin-bottom:10px;background:#0d1117;color:white;border:1px solid #30363d;border-radius:6px;";
    
    const dropdown = document.createElement("select");
    dropdown.innerHTML = `
        <option value="5">Top 5</option>
        <option value="10" selected>Top 10</option>
        <option value="20">Top 20</option>
    `;
    dropdown.style = "margin-left:10px;padding:8px;background:#0d1117;color:white;border:1px solid #30363d;border-radius:6px;";

    document.querySelector(".container").prepend(searchBox, dropdown);

    function renderCharts(data) {

        const labels = data.map(d => d.file);
        const riskValues = data.map(d => d.priority_score);
        const bugValues = data.map(d => d.bug_density);

        // KPIs
        document.getElementById("kpi-files").innerText = data.length;

        const avg = (riskValues.reduce((a,b)=>a+b,0)/riskValues.length).toFixed(1);
        document.getElementById("kpi-risk").innerText = avg;

        const high = data.filter(d => d.priority_score > 80).length;
        document.getElementById("kpi-high").innerText = high;

        const colors = data.map(d => {
            if (d.severity === "CRITICAL") return "#ff4d4f";
            if (d.severity === "HIGH") return "#fa8c16";
            if (d.severity === "MEDIUM") return "#fadb14";
            return "#52c41a";
        });

        // destroy previous chart (IMPORTANT)
        if (chartInstance) chartInstance.destroy();

        chartInstance = new Chart(document.getElementById("riskChart"), {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    data: riskValues,
                    backgroundColor: colors
                }]
            },
            options: {
                plugins: { legend: { display: false } },
                onClick: (e, elements) => {
                    if (elements.length > 0) {
                        const index = elements[0].index;
                        const file = labels[index];

                        fetch(`/file-detail?file=${file}`)
                        .then(res => res.json())
                        .then(data => {
                            alert(`File: ${file}\nChurn: ${data.churn}`);
                        });
                    }
                }
            }
        });

        new Chart(document.getElementById("bugChart"), {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    data: bugValues,
                    backgroundColor: "#58a6ff"
                }]
            },
            options: { plugins: { legend: { display: false } } }
        });
    }

    function applyFilters() {

        if (!Array.isArray(fullData)) return; // safety

        const query = searchBox.value.toLowerCase();
        const limit = parseInt(dropdown.value);

        let filtered = fullData.filter(d =>
            d.file.toLowerCase().includes(query)
        );

        filtered = filtered.slice(0, limit);

        renderCharts(filtered);
    }

    function loadData() {
        fetch('/bug-risk')
        .then(res => res.json())
        .then(data => {

            console.log("RAW DATA:", data);

            
            if (!Array.isArray(data)) {
                console.error("Expected array but got:", data);
                return;
            }

            fullData = data;
            applyFilters();
        })
        .catch(err => console.error("Fetch error:", err));
    }

    // -------- INITIAL LOAD --------
    loadData();

    // -------- SEARCH --------
    searchBox.addEventListener("input", applyFilters);

    // -------- DROPDOWN --------
    dropdown.addEventListener("change", applyFilters);

    // -------- LIVE REFRESH --------
    setInterval(() => {
        console.log(" refreshing...");
        loadData();
    }, 10000);

    // -------- DEVELOPERS --------
    fetch('/developers')
    .then(res => res.json())
    .then(devData => {
        new Chart(document.getElementById("devChart"), {
            type: 'bar',
            data: {
                labels: devData.map(d => d.name),
                datasets: [{
                    data: devData.map(d => d.score),
                    backgroundColor: "#58a6ff"
                }]
            },
            options: { plugins: { legend: { display: false } } }
        });
    });

    // -------- TIMELINE --------
    fetch('/risk-timeline')
    .then(res => res.json())
    .then(timeData => {
        new Chart(document.getElementById("timeChart"), {
            type: 'line',
            data: {
                labels: timeData.map(d => d.month),
                datasets: [{
                    data: timeData.map(d => d.churn),
                    borderColor: "#58a6ff",
                    fill: false
                }]
            },
            options: { plugins: { legend: { display: false } } }
        });
    });

});
</script>
</body>
</html>
"""