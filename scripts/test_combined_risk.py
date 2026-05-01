from app.storage.db import SessionLocal
from app.analysis.combined_risk import get_combined_risk


def classify(score):
    if score > 5000:
        return "HIGH"
    elif score > 2000:
        return "MEDIUM"
    else:
        return "LOW"


def test_combined():
    session = SessionLocal()

    results = get_combined_risk(session)

    max_score = max(score for _, score in results)

    for name, score in results:
        normalized = (score / max_score) * 100
        print(f"{name:<25} | score={round(normalized,2):<6} /100")
        session.close()


if __name__ == "__main__":
    test_combined()