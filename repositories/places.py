from flaskr.db import db, Place, Tag
from sqlalchemy import Select



def add(name: str, address: str, map_link: str, travel_time_min: int, extra_info: str, tag_ids: list[int]) -> None:

    # replace tag-id for coresponding tag
    tags = db.session.scalars(
        db.select(Tag).where(Tag.tag_id.in_(tag_ids))
    ).all()

    # all tag_ids must exist in database
    if len(tags) != len(set(tag_ids)):
        raise ValueError("One or more tag IDs do not exist.")

    #create place object
    place = Place(
        place_name = name,
        address = address,
        map_link = map_link,
        travel_time_min = travel_time_min,
        extra_info = extra_info,
        tags = tags
    )

    db.session.add(place)


def delete(place: int) -> None:
    # if user is int: get user object for coresponding id
    #if isinstance(place, int):
    place = by_id(place)
    
    db.session.delete(place)


def by_id(id: int) -> Place:
    place = db.get_or_404(Place, id, description="Place not found")
    return place


def by_name(place_name: str) -> Place:
    command = db.select(Place).where(Place.place_name == place_name)
    place = db.session.scalars(command).one_or_none()
    
    return place


def by_name_search(query: str) -> list[Place]:
    command = db.select(Place).where(Place.place_name.like(f"%{query}%"))
    places = db.session.scalars(command).all()

    return places

def by_tags(*tag_ids: list[int]):
    command = db.select(Place).where(
        *[
            Place.tags.any(Tag.tag_id == tag_id)
            for tag_id in tag_ids
        ]
    )

    places = db.session.scalars(command).all()

    return places

def commit_changes():
    db.session.commit()