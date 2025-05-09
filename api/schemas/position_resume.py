from pydantic import BaseModel


class Position(BaseModel):
    title = str
    company = str
    location = str
    description = str