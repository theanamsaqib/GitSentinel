from app.storage.db import SessionLocal
from app.analysis.developer_risk import get_developer_risk


def classify(churn):
    if churn > 2000:
        return "HIGH"
    elif churn > 1000:
        return "MEDIUM"
    else:
        return "LOW"


def test_dev_risk():
    session = SessionLocal()

    results = get_developer_risk(session)

    for name, commits, churn in results:
        level = classify(churn)
        print(f"{name:<25} | commits={commits:<5} | churn={churn:<6} | {level}")

    session.close()


if __name__ == "__main__":
    test_dev_risk()