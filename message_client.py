from services.api.v1.message_service.service import message_run


if __name__ == "__main__":
    import asyncio

    asyncio.run(message_run())
