from fastapi import APIRouter, Request, Depends, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import config
from app.data.db import SessionDep
from app.models.event import Event, EventRead
from sqlmodel import select, Session,delete
from typing import List, Annotated
from app.models.user import User
from app.models.registration import Registration


router = APIRouter(prefix="/events", tags=["events"],)


# Definisci prima tutti gli endpoint GET
@router.get("/", response_model=List[EventRead])
def get_events(db: SessionDep):
    statement = select(Event)
    events = db.exec(statement).all()
    return events

@router.post("/")
def create_event(event: Event, session: SessionDep):
    """Adds a new event."""
    validated_event = Event.model_validate(event)
    session.add(validated_event)
    session.commit()
    return "Event successfully added."

@router.delete("/", status_code=200)
def delete_all_events(session: SessionDep):
    statement = delete(Event)
    session.exec(statement)
    session.commit()
    return "All events deleted"

@router.get("/{id}", response_model=EventRead)
def get_event(db: SessionDep, id: int = Path(...)):
    statement = select(Event).where(Event.id == id)
    event = db.exec(statement).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
