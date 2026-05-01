from app.storage.db import SessionLocal
from app.analysis.bug_metrics import get_file_bug_metrics

session = SessionLocal()
results = get_file_bug_metrics(session)

for file, total, bugs, density in results:
    print(f"{file:<40} | bugs={bugs}/{total} | density={round(density,2)}")

session.close()