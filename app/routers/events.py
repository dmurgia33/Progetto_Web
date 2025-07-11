from fastapi import APIRouter, HTTPException, Path
from app.data.db import SessionDep
from app.models.event import Event, EventRead, EventCreate
from sqlmodel import select, delete
from typing import List, Annotated
from app.models.user import User, UserCreate
from app.models.registration import Registration



router = APIRouter(prefix="/events", tags=["events"])

#GET /events/ - Lista eventi
@router.get("/", response_model=List[EventRead])
def get_events(session: SessionDep):
    statement = select(Event)
    events = session.exec(statement).all()
    return events

#POST /events/ - Crea un nuovo evento
@router.post("/", response_model=EventRead, status_code=201)
def create_event(event: EventCreate, session: SessionDep):
    """Adds a new event and returns it (with id)."""
    new_event = Event(**event.dict())
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return new_event

#Endpoint DELETE /events/ – Elimina tutti gli eventi
@router.delete("/", status_code=200)
def delete_all_events(session: SessionDep):
    statement = delete(Event)
    session.exec(statement)
    session.commit()
    return "All events deleted"

#DELETE /events/{id} – Elimina un evento specifico
@router.delete("/{id}", status_code=204)
def delete_event(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the event to delete")]
):
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(event)
    session.commit()

#GET /events/{id} - Mostra un evento specifico
@router.get("/{id}", response_model=EventRead)
def get_event(session: SessionDep, id: int = Path(...)):
    statement = select(Event).where(Event.id == id)
    event = session.exec(statement).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
    
#PUT /events/{id} – Aggiorna un evento specifico
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

#POST /events/{id}/register – Registra un utente a un evento
@router.post("/{id}/register")
def register_user_to_event(
    *,
    id: int = Path(..., description="The ID of the event"),
    user_data: UserCreate,
    session: SessionDep
):
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    user = session.get(User, user_data.username)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")


    statement = select(Registration).where(
        (Registration.event_id == id) & (Registration.username == user.username)
    )
    existing_registration = session.exec(statement).first()
    if existing_registration:
        raise HTTPException(status_code=400, detail="User already registered for this event")

    registration = Registration(username=user.username, event_id=id)
    session.add(registration)
    session.commit()

    return {"message": f"User '{user.username}' successfully registered for event {id}"}
