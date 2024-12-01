from services.api.v1.chat_service.service import chat_run


if __name__ == "__main__":
    import asyncio

    asyncio.run(chat_run())
