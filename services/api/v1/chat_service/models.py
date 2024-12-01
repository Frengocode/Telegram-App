from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Integer
from database.chat_database import ChatBase


class ChatModel(ChatBase):
    __tablename__ = "chats"

    chat_author_id: Mapped[int] = mapped_column(Integer, nullable=True)
    chat_member_id: Mapped[int] = mapped_column(Integer, nullable=True)
