from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)

class User(db.Model):
  __tablename__ = "users"
  user_id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(unique=True, nullable=False)
  pass_salt: Mapped[bytes] = mapped_column(nullable=False)
  pass_hash_sha256: Mapped[str] = mapped_column(nullable=False)
  is_admin: Mapped[bool] = mapped_column(nullable=False)


class Place(db.Model):
  __tablename__ = "places"
  place_id: Mapped[int] = mapped_column(primary_key=True)
  place_name: Mapped[str] = mapped_column(unique=True, nullable=False)
  address: Mapped[str] = mapped_column(nullable=False)
  map_link: Mapped[str] = mapped_column(nullable=False)
  travel_time_min: Mapped[int] = mapped_column(nullable=False)
  extra_info: Mapped[str] = mapped_column(nullable=False)


class Tag(db.Model):
  __tablename__ = "tags"
  tag_id: Mapped[int] = mapped_column(primary_key=True)
  tag_name: Mapped[str] = mapped_column(nullable=False)




