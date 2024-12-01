from pydantic import BaseModel
from typing import Optional


class CreateChatRequest(BaseModel):
    member_id: int
