from pydriller import Repository
from app.storage.db import SessionLocal
from app.processor.ingest import ingest_commit


def run_ingestion():
    print(" ...STARTING INGESTION...")

    session = SessionLocal()
    repo_path = "gson"

    count = 0
    max_commits = 100   

    for commit in Repository(repo_path).traverse_commits():
        print("PROCESSING:", commit.hash)

        data = {
            "hash": commit.hash,
            "author_name": commit.author.name,
            "author_email": commit.author.email,
            "date": commit.author_date,
            "message": commit.msg,
            "files": []
        }

        for mod in commit.modified_files:
            if not mod.filename:
                continue

            data["files"].append({
                "filename": mod.filename,
                "added": mod.added_lines or 0,
                "deleted": mod.deleted_lines or 0
            })

        try:
            ingest_commit(session, repo_path, data)
            count += 1

            print(f"✅ Inserted {count}")

            if count >= max_commits:
                print(" ...STOPPING...")
                break

        except Exception as e:
            print("ERROR:", e)

    session.close()
    print(" ...DONE WITH INGESTION...")


if __name__ == "__main__":
    run_ingestion()