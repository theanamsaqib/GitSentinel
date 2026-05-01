from app.models.file import File

def get_or_create_file(session, repo_id, file_path):
    file = session.query(File).filter_by(
        repo_id=repo_id,
        file_path=file_path
    ).first()

    if file:
        return file

    file = File(repo_id=repo_id, file_path=file_path)
    session.add(file)
    session.flush()
    session.refresh(file)

    return file