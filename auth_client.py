from services.api.v1.auth_service.service import auth_run


if __name__ == "__main__":
    import asyncio

    asyncio.run(auth_run())
