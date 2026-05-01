from app.storage.db import SessionLocal
from app.analysis.time_risk import get_risk_over_time

session = SessionLocal()
results = get_risk_over_time(session)

for month, churn in results:
    print(month, churn)

session.close()