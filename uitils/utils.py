from passlib.context import CryptContext
from datetime import datetime, timedelta
import colorlog
import logging
from jose import jwt
from redis.asyncio import StrictRedis
from core.config import SECRET_KEY


ALGORITHM = "HS256"
SECRET_KEY = SECRET_KEY
ACCESS_TOKEN_EXPIRE_DAYS = 360


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

handler = colorlog.StreamHandler()

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
    log_colors={
        "DEBUG": "blue",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)

handler.setFormatter(formatter)

log.addHandler(handler)


pwd_context = CryptContext(schemes=["bcrypt"])


class Hash:

    @staticmethod
    def bcrypt(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()

    # Проверка, чтобы 'sub' был строкой
    if not isinstance(to_encode.get("sub"), str):
        raise ValueError("Subject (sub) must be a string")

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_redis_client() -> StrictRedis:
    return StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
