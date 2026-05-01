from app.storage.db import SessionLocal
from app.analysis.risk import get_file_risk_scores


def classify(risk):
    if risk > 2000:
        return "HIGH"
    elif risk > 1000:
        return "MEDIUM"
    else:
        return "LOW"


def test_risk():
    session = SessionLocal()

    results = get_file_risk_scores(session)

    for file_path, count, churn, bug_density, risk in results:
        level = classify(risk)
        print(f"{file_path:<40} | risk={round(risk,2):<8} | bugs={round(bug_density,2)} | {level}")

    session.close()


if __name__ == "__main__":
    test_risk()