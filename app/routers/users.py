from fastapi import APIRouter, HTTPException, Path
from app.data.db import SessionDep
from app.models.event import Event, EventRead, EventCreate
from sqlmodel import select, delete
from typing import List, Annotated
from app.models.user import User, UserRead, UserCreate


router = APIRouter(prefix="/users", tags=["users"],)



#GET /users/ - Elenco utenti
@router.get("/", response_model=List[UserRead])
def get_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users



#POST /users/ - Crea nuovo utente
@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, session: SessionDep):
    existing = session.get(User, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

#GET /users/{username} - Ottieni utente per username
@router.get("/{username}", response_model=UserRead)
def get_user_by_username(username: Annotated[str, Path()], session: SessionDep):
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#DELETE /users/ — Elimina tutti gli utenti
@router.delete("/", status_code=200)
def delete_all_users(session: SessionDep):
    session.exec(delete(User))
    session.commit()
    return {"message": "All users have been deleted"}

#DELETE /users/{username} — Elimina utente specifico
@router.delete("/{username}", status_code=200)
def delete_user_by_username(username: Annotated[str, Path()], session: SessionDep):
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": f"User '{username}' has been deleted"}

