from app.storage.db import SessionLocal
from app.analysis.hotspots import get_hotspot_files

def test_analysis():
    session = SessionLocal()

    results = get_hotspot_files(session)

    for row in results:
        print(row)

    session.close()

if __name__ == "__main__":
    test_analysis()