from services.api.v1.user_service.service import run
from services.api.v1.auth_service.service import auth_run


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
    asyncio.run(auth_run())
