from pydantic import BaseModel


class CreateHistoryRequestScheme(BaseModel):
    content_title: str
