from fastapi import APIRouter, Request, Depends, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from config import config
from data.db import SessionDep
from models.event import Event, EventRead, EventCreate
from sqlmodel import select, Session,delete
from typing import List, Annotated
from models.user import User
from models.registration import Registration


router = APIRouter(prefix="/events", tags=["events"],)


# Definisci prima tutti gli endpoint GET

@router.get("/", response_model=List[EventRead])
def get_events(session: SessionDep):
    statement = select(Event)
    events = session.exec(statement).all()
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

@router.delete("/{id}", status_code=204)
def delete_event(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the event to delete")]
):
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    print(f"Deleting event: {event}")  # debug
    session.delete(event)
    session.commit()
    print("Event deleted and committed")  # debug

@router.get("/{id}", response_model=EventRead)
def get_event(session: SessionDep, id: int = Path(...)):
    statement = select(Event).where(Event.id == id)
    event = session.exec(statement).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{id}", response_model=EventRead)
def update_event(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the event to update")],
    new_event: EventCreate
):
    """Updates the event with the given ID."""
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    event.title = new_event.title
    event.description = new_event.description
    event.date = new_event.date
    event.location = new_event.location

    session.add(event)
    session.commit()
    session.refresh(event)

    return event

@router.post("/{id}/register")
def register_user_to_event(
    *,
    id: int = Path(..., description="The ID of the event"),
    user_data: User,
    session: SessionDep
):
    # Controlla che l'evento esista
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Cerca l'utente per username
    user = session.get(User, user_data.username)

    if user is None:
        # Utente non esiste: crea nuovo utente con i dati inviati
        user = User(username=user_data.username, name=user_data.name, email=user_data.email)
        session.add(user)
        session.commit()
        session.refresh(user)
    else:
        # Utente esiste, NON modificare nome/email
        pass

    # Controlla se l'utente è già registrato all'evento
    statement = select(Registration).where(
        (Registration.event_id == id) &
        (Registration.username == user.username)
    )
    existing_registration = session.exec(statement).first()
    if existing_registration:
        raise HTTPException(status_code=400, detail="User already registered for this event")

    # Crea la registrazione
    registration = Registration(username=user.username, event_id=id)
    session.add(registration)
    session.commit()

    return {"message": f"User '{user.username}' successfully registered for event {id}"}

