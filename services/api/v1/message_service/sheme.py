from pydantic import BaseModel
from typing import Optional, Annotated



class CreateMessageRequestScheme(BaseModel):
    message: str
    chat_id: int
    