from fastapi import FastAPI
from services.api.v1.user_service.router import user_serivce_router
from services.api.v1.auth_service.router import auth_service_router
from services.api.v1.chat_service.router import chat_service_router
from services.api.v1.message_service.router import message_service_router

from fastapi.middleware.cors import CORSMiddleware
from database.chat_database import ChatBase, chat_engine
from database.message_database import MessageBase, message_engine


app = FastAPI(title="Telegram App")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_serivce_router)
app.include_router(auth_service_router)
app.include_router(chat_service_router)
app.include_router(message_service_router)


async def create_teables():
    async with message_engine.begin() as conn:
        await conn.run_sync(MessageBase.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    return await create_teables()
