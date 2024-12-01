from pydantic import BaseModel
from typing import Optional


class SUser(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    profile_picture: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[str] = None
    token: Optional[str] = None
