from app.storage.repositories import get_or_create_repository
from app.storage.developers import get_or_create_developer
from app.storage.commits import insert_commit
from app.storage.files import get_or_create_file
from app.storage.file_changes import insert_file_change


def ingest_commit(session, repo_url, commit_data):
    try:
        print("🔥 Ingesting:", commit_data["hash"])

        # 1. repository
        repo = get_or_create_repository(session, "repo", repo_url)

        # 2. developer
        dev = get_or_create_developer(
            session,
            commit_data["author_name"],
            commit_data["author_email"]
        )

        # 3. commit
        db_commit = insert_commit(session, {
            "hash": commit_data["hash"],
            "repo_id": repo.id,
            "author_id": dev.id,
            "commit_date": commit_data["date"],
            "message": commit_data["message"]
        })

        # 4. file changes
        for file in commit_data["files"]:
            db_file = get_or_create_file(
                session,
                repo.id,
                file["filename"]
            )

            insert_file_change(session, {
                "commit_hash": db_commit.hash,
                "file_id": db_file.id,
                "lines_added": file["added"],
                "lines_deleted": file["deleted"]
            })

        # 5. commit transaction
        print("💾 committing:", commit_data["hash"])
        session.commit()

    except Exception as e:
        session.rollback()
        print("❌ REAL ERROR:", e)