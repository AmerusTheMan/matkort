from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column

class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)



places_tags = db.Table(
  "places_tags",
  db.Model.metadata,
  Column("place_id", db.ForeignKey("places.place_id", ondelete="CASCADE")),
  Column("tag_id", db.ForeignKey("tags.tag_id", ondelete="CASCADE"))
)

class Place(db.Model):
  __tablename__ = "places"
  place_id: Mapped[int] = mapped_column(primary_key=True)
  place_name: Mapped[str] = mapped_column(unique=True, nullable=False)
  address: Mapped[str] = mapped_column(nullable=False)
  map_link: Mapped[str] = mapped_column(nullable=False)
  travel_time_min: Mapped[int] = mapped_column(nullable=False)
  extra_info: Mapped[str] = mapped_column(nullable=False)

  tags: Mapped[list["Tag"]] = relationship(
    secondary=places_tags,
    back_populates="places"
  )

  def __repr__(self):
    return (self.place_name)


class Tag(db.Model):
  __tablename__ = "tags"
  tag_id: Mapped[int] = mapped_column(primary_key=True)
  tag_name: Mapped[str] = mapped_column(nullable=False)

  places: Mapped[list['Place']] = relationship(
    secondary=places_tags,
    back_populates="tags"
  )

  def __repr__(self):
    return self.tag_name


class User(db.Model):
  __tablename__ = "users"
  user_id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(unique=True, nullable=False)
  pass_salt: Mapped[bytes] = mapped_column(nullable=False)
  pass_hash_sha256: Mapped[str] = mapped_column(nullable=False)
  is_admin: Mapped[bool] = mapped_column(nullable=False)

  def __repr__(self):
    return self.username