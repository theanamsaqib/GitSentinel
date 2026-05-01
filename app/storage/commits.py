from app.models.commit import Commit  


def insert_commit(session, commit_data):
    existing = session.query(Commit).filter_by(hash=commit_data["hash"]).first()

    if existing:
        print("SKIPPING existing commit:", commit_data["hash"])
        return existing

    print("INSERTING commit:", commit_data["hash"])

    db_commit = Commit(**commit_data)
    session.add(db_commit)
    session.flush()  

    return db_commit