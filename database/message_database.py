from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from datetime import datetime
from core.config import PG_HOST, PG_PASSWORD, PG_USERNAME
from sqlalchemy import Integer, DateTime


DATABASE_URL = f"postgresql+asyncpg://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOST}/MessageTDB"

message_engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(class_=AsyncSession, bind=message_engine)


class MessageBase(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())


async def get_message_sesison() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
