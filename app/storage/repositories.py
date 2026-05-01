from app.models.repository import Repository

def get_or_create_repository(session, name, url):
    repo = session.query(Repository).filter_by(url=url).first()

    if repo:
        return repo

    repo = Repository(name=name, url=url)
    session.add(repo)
    session.flush()  

    return repo