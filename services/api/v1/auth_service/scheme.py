from pydantic import BaseModel


class LoginRequestScheme(BaseModel):
    username: str
    password: str
