from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, sessionmaker
from sqlalchemy import Integer, DateTime
from core.config import settings
from datetime import datetime


DATABASE_URL = f"postgresql+asyncpg://{settings.database.username}:{settings.database.password.get_secret_value()}@{settings.database.host}/HistoryDBT"

history_engine = create_async_engine(DATABASE_URL)

session = sessionmaker(class_=AsyncSession, bind=history_engine)


class HistoryBase(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
