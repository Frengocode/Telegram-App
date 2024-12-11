from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database.history_database import HistoryBase


class HistoryModel(HistoryBase):
    __tablename__ = "histories"

    content_title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
