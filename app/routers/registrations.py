from fastapi import APIRouter, Query, HTTPException
from typing import List
from app.data.db import SessionDep
from app.models.registration import Registration
from app.models.registration import RegistrationRead
from sqlmodel import select

router = APIRouter(prefix="/registrations", tags=["registrations"])

#GET /registrations/ — Elenco registrazioni
@router.get("/", response_model=List[RegistrationRead])
def get_registrations(session: SessionDep):
    registrations = session.exec(select(Registration)).all()
    return registrations

#DELETE /registrations/ — Elimina una registrazione specifica
@router.delete("/", status_code=204)
def delete_registration(
    username: str = Query(..., description="The username of the registration to delete"),
    event_id: int = Query(..., description="The event_id of the registration to delete"),
    session: SessionDep = None
):
    # Trova la registrazione corrispondente
    statement = select(Registration).where(
        Registration.username == username,
        Registration.event_id == event_id
    )
    registration = session.exec(statement).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    session.delete(registration)
    session.commit()
