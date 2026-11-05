from flaskr.db import db, Tag


def add(name: str) -> None:
    tag = Tag(tag_name = name)
    db.session.add(tag)


def delete(tag: int) -> None:
    tag = by_id(tag)
    
    db.session.delete(tag)


def by_id(id: int) -> Tag:
    tag = db.get_or_404(Tag, id, description="Place not found")
    return tag


def by_name(tag_name: str) -> Tag:
    command = db.select(Tag).where(Tag.tag_name == tag_name)
    tag = db.execute(command).scalar_one_or_none()
    return tag

def by_name_search(query: str) -> list[Tag]:
    command = db.select(Tag).where(Tag.tag_name.like(f"%{query}%"))
    tags = db.session.execute(command).scalars().all()
    return tags




