from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from datetime import datetime
from core.config import settings
from sqlalchemy import Integer, DateTime


DATABASE_URL = f"postgresql+asyncpg://{settings.database.username}:{settings.database.password.get_secret_value()}@{settings.database.host}/ChatT"

chat_engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(class_=AsyncSession, bind=chat_engine)


class ChatBase(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())


async def get_chat_sesison() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
