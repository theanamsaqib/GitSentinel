from app.models.file_changes import FileChange

def insert_file_change(session, data):
    fc = FileChange(**data)
    session.add(fc)
   