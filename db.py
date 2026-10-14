from main import db
from sqlalchemy.orm import Mapped, mapped_column


class User(db.Model):
  __tablename__ = "users"
  user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  username: Mapped[str] = mapped_column(unique=True)
  pass_salt: Mapped[str] = mapped_column()
  pass_hash_sha256: Mapped[str] = mapped_column()
  is_admin: Mapped[bool] = mapped_column()


class Place(db.Model):
  __tablename__ = "places"
  place_id: Mapped[id] = mapped_column(primary_key=True, autoincrement=True)
  place_name: Mapped[str] = mapped_column(unique=True)
  address: Mapped[str] = mapped_column()
  map_link: Mapped[str] = mapped_column()
  travel_time_min: Mapped[int] = mapped_column()
  extra_info: Mapped[str] = mapped_column()


class Tag(db.Model):
  __tablename__ = "tags"
  tag_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  tag_name: Mapped[str] = mapped_column()
  tag_type_id: Mapped[str]




