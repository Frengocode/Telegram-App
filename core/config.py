from dotenv import load_dotenv
from pydantic import BaseModel, SecretStr
import os

load_dotenv()


class DatabaseConfig(BaseModel):
    username: str
    password: SecretStr
    host: str


class AuthSettings(BaseModel):
    secret_key: SecretStr


class Setting(BaseModel):
    auth: AuthSettings
    database: DatabaseConfig


settings = Setting(
    auth=AuthSettings(secret_key=os.getenv("SECRET_KEY")),
    database=DatabaseConfig(
        username=os.getenv("PG_USERNAME"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST"),
    ),
)
