import hashlib
from os import urandom
from flaskr.db import db, User


def random_salt(length=32) -> bytes:
    salt = urandom(length)
    return salt

def sha256(data: bytes):
    return hashlib.sha256(data).hexdigest()


def add(username: str, password: str, is_admin: bool) -> None:
    salt = random_salt()
    salted_password = salt+password.encode()
    hash = sha256(salted_password)

    user = User(
        username=username,
        pass_salt=salt,
        pass_hash_sha256=hash,
        is_admin=is_admin
    )

    db.session.add(user)


def delete(user: int) -> None:
    user = by_id(user)
    
    db.session.delete(user)


def by_id(id: int) -> User:
    user = db.get_or_404(User, id, description="User not found")
    return user


def by_name(username: str) -> User:
    command = db.select(User).where(User.username == username)
    print(command)
    user = db.session.execute(command).scalar_one_or_none()
    
    return user


def by_name_search(query: str) -> list[User]:
    command = db.select(User).where(User.username.like(f"%{query}%"))
    users = db.session.execute(command).scalars().all()
    return users


def attempt_login(user: User, password: str) -> bool:
    salted_attempt = user.pass_salt + password.encode()
    attempt_hash = sha256(salted_attempt)

    return attempt_hash == user.pass_hash_sha256


def commit_changes():
    db.session.commit()
