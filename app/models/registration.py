from sqlmodel import SQLModel, Field

class Registration(SQLModel, table=True):
    username: str = Field(primary_key=True, foreign_key="user.username", ondelete="CASCADE")
    event_id: int = Field(primary_key=True, foreign_key="event.id", ondelete="CASCADE")


class RegistrationCreate(SQLModel):
    username: str
    event_id: int


class RegistrationRead(SQLModel):
    username: str
    event_id: int
