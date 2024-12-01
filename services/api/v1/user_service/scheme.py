from pydantic import BaseModel


class CreateUserSceheme(BaseModel):
    username: str
    password: str
    email: str
    name: str
