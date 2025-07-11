from sqlmodel import SQLModel, Field
from typing import Optional


class Event(SQLModel, table=True):
    __table_args__ = {'sqlite_autoincrement': True}
    '''Senza sqlite_autoincrement, SQLite assegna il più piccolo ID disponibile. 
    Con sqlite_autoincrement posto a True, SQLite continua sempre a incrementare l’ultimo ID massimo usato.'''
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    date: str
    location: str


class EventCreate(SQLModel):
    # Non include 'id' perché verrà generato automaticamente
    title: str
    description: str
    date: str
    location: str

class EventRead(SQLModel):
    # Include l'ID, che è noto solo dopo la creazione
    id: int
    title: str
    description: str
    date: str
    location: str
