from fastapi import FastAPI
from services.api.v1.user_service.router import user_serivce_router
from services.api.v1.auth_service.router import auth_service_router
from services.api.v1.chat_service.router import chat_service_router
from services.api.v1.message_service.router import message_service_router
from services.api.v1.history_service.router import history_service_router
from database.chat_database import chat_engine, ChatBase
from database.user_database import user_engine, UserBase

from fastapi.middleware.cors import CORSMiddleware
from database.chat_database import ChatBase, chat_engine
from database.message_database import MessageBase, message_engine
from database.history_database import HistoryBase, history_engine




app = FastAPI(title="Telegram App")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_serivce_router)
app.include_router(auth_service_router)
app.include_router(chat_service_router)
app.include_router(message_service_router)
app.include_router(history_service_router)




# async def create_teables():
#     async with message_engine.begin() as conn:
#         await conn.run_sync(MessageBase.metadata.create_all)


async def create_teables():
    async with message_engine.begin() as conn:
        await conn.run_sync(MessageBase.metadata.create_all)
    
    async with user_engine.begin() as conn:
        await conn.run_sync(UserBase.metadata.create_all)

    async with history_engine.begin() as conn:
        await conn.run_sync(HistoryBase.metadata.create_all)

    async with chat_engine.begin() as conn:
        await conn.run_sync(ChatBase.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    return await create_teables()
