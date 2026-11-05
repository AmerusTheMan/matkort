from flaskr.db import db

def commit_changes() -> None:
    db.session.commit()