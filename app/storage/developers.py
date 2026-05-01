from app.models.developer import Developer

def get_or_create_developer(session, name, email):
    dev = session.query(Developer).filter_by(email=email).first()

    if dev:
        return dev

    dev = Developer(name=name, email=email)
    session.add(dev)
    session.flush()
    session.refresh(dev)

    return dev