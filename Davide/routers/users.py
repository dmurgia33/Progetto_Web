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


router = APIRouter(prefix="/users", tags=["users"],)

# Definisci prima tutti gli endpoint GET

@router.get("/", response_model=List[User])
def get_users(session: SessionDep):
    statement = select(User)
    users = session.exec(statement).all()
    return users

@router.post("/", response_model=User)
def create_user(user:User,session:SessionDep):
    existing=session.get(User,user.username)
    if existing:
        raise HTTPException(status_code=400,detail="Username già esistente")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/{username}",response_model=User)
def get_user_by_username(username:Annotated[str,Path()],session:SessionDep):
    user=session.get(User,username)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    return user

@router.delete("/", status_code=200)
def delete_all_users(session:SessionDep):
    session.exec(delete(User))
    session.commit()
    return {"Tutti gli utenti sono stati eliminati"}

@router.delete("/{username}",status_code=200)
def delete_user_by_username(username:Annotated[str,Path()],session:SessionDep):
    user=session.get(User,username)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    session.delete(user)
    session.commit()
    return {f"Utente '{username}' eliminato"}


