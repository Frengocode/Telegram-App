from pydantic import BaseModel


class CreateUserSceheme(BaseModel):
    username: str
    password: str
    email: str
    name: str


class UpdateProfileRequestScheme(BaseModel):
    username: str
    name: str
    email: str
    surname: str
