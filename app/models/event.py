from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Event(SQLModel, table=True):
    __table_args__ = {'sqlite_autoincrement': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    date: str
    location: str


class EventCreate(SQLModel):
    title: str
    description: str
    date: str
    location: str

class EventRead(SQLModel):
    id: int
    title: str
    description: str
    date: str
    location: str
