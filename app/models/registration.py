from sqlmodel import SQLModel, Field

class Registration(SQLModel, table=True):
    username: str = Field(primary_key=True, foreign_key="user.username", ondelete="CASCADE") # se l'utente viene eliminato, elimina anche le sue registrazioni
    event_id: int = Field(primary_key=True, foreign_key="event.id", ondelete="CASCADE") # se l'evento viene eliminato, elimina anche le registrazioni collegate


class RegistrationCreate(SQLModel):
    username: str
    event_id: int


class RegistrationRead(SQLModel):
    username: str
    event_id: int
