from sqlalchemy import String, Integer
from database.user_database import UserBase
from sqlalchemy.orm import mapped_column, Mapped


class UserModel(UserBase):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, nullable=False)
    picture_url: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
