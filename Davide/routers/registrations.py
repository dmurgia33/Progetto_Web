from fastapi import APIRouter
from typing import List
from app.data.db import SessionDep
from app.models.registration import Registration
from app.models.registration import RegistrationRead
from sqlmodel import select

router = APIRouter()

@router.get("/registrations", response_model=List[RegistrationRead])
def get_registrations(session: SessionDep):
    registrations = session.exec(select(Registration)).all()
    return registrations
