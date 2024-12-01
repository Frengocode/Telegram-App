from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Integer, Boolean
from database.message_database import MessageBase



class MessageModel(MessageBase):
    __tablename__ = "messages"

    message: Mapped[str] = mapped_column(String, nullable=False)
    chat_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_updated: Mapped[bool] = mapped_column(Boolean, default=False)
    