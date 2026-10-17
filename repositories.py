import hashlib
from database import db, User, Place, Tag
from os import urandom
from sqlalchemy import select


def random_salt(length=32) -> bytes:
    salt = urandom(length)
    return salt

def sha256(data: bytes):
    return hashlib.sha256(data).hexdigest()


class users:
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


    def delete(user: User | int) -> None:
        if isinstance(user, int):
            user = self.by_id(user)
        
        db.session.delete(user)


    def by_id(id: int) -> User:
        user = db.get_or_404(User, id, description="User not found")
        return user


    def by_name(username: str) -> User:
        command = select(User).where(User.username == username)
        print(command)
        user = db.session.execute(command).scalar_one_or_none()
        
        return user


    def by_name_search(query: str) -> list[User]:
        command = select(User).where(User.username.like(f"%{query}%"))
        users = db.session.execute(command).scalars().all()
        return users


    def attempt_login(user: User, password: str) -> bool:
        salted_attempt = user.pass_salt + password.encode()
        attempt_hash = sha256(salted_attempt)

        return attempt_hash == user.pass_hash_sha256


    def commit_changes():
        db.session.commit()



class places:
    def add(name: str, address: str, map_link: str, travel_time_min: int, extra_info: str) -> None:
        place = Place(
            place_name = name,
            address = address,
            map_link = map_link,
            travel_time_min = travel_time_min,
            extra_info = extra_info
        )

        db.session.add(place)


    def delete(user: Place | int) -> None:
        if isinstance(place, int):
            place = self.by_id(place)
        
        db.session.delete(place)


    def by_id(id: int) -> Place:
        place = db.get_or_404(Place, id, description="Place not found")
        return place


    def by_name(place_name: str) -> Place:
        command = select(Place).where(Place.place_name == place_name)
        place = db.session.execute(command).scalar_one_or_none()
        
        return place


    def by_name_search(query: str) -> list[Place]:
        command = select(Place).where(Place.place_name.like(f"%{query}%"))
        places = db.session.execute(command).scalars().all()
        return places


    def commit_changes():
        db.session.commit()



class tags:
    def add(name: str) -> None:
        tag = Tag(tag_name = name)
        db.session.add(tag)


    def delete(tag: Tag | int) -> None:
        if isinstance(place, int):
            tag = self.by_id(tag)
        
        db.session.delete(user)


    def by_name(tag_name: str) -> Tag:
        command = select(Tag).where(Tag.tag_name == tag_name)
        tag = db.execute(command).scalar_one_or_none()
        return tag

    def by_name_search(query: str) -> list[Tag]:
        command = select(Tag).where(Tag.tag_name.like(f"%{query}%"))
        tags = db.session.execute(command).scalars().all()
        return tags

    def commit_changes() -> None:
        db.session.commit()

    