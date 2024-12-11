from services.api.v1.history_service.service import history_run


if __name__ == "__main__":
    import asyncio

    asyncio.run(history_run())
