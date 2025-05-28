from fastapi import APIRouter, Request, Depends, status, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import config
from app.data.db import SessionDep
from app.models.event import Event, EventRead
from sqlmodel import select, Session
from typing import List
from app.models.user import User
from app.models.registration import Registration

router = APIRouter()
templates = Jinja2Templates(directory=config.root_dir / "templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html",
    )


@router.get("/events_list", response_class=HTMLResponse)
async def events_list(request: Request):
    return templates.TemplateResponse(
        request=request, name="events.html",
    )


@router.get("/event_detail/{id}", response_class=HTMLResponse)
async def event_detail(request: Request, id: int):
    return templates.TemplateResponse(
        request=request, name="event_detail.html",
        context={"event_id": id},
    )


@router.get("/users_list", response_class=HTMLResponse)
async def users_list(request: Request):
    return templates.TemplateResponse(
        request=request, name="users.html"
    )


''' 
Creazione prime 4 API
'''


@router.get("/events", response_model=List[EventRead])
def get_events(db: SessionDep):
    return db.query(Event).all()


@router.post("/events", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(event: Event, db: SessionDep):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.get("/events/{id}", response_model=EventRead)
def get_event(db: SessionDep, id: int = Path(...)):
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.delete("/events", status_code=204)
def delete_all_events(db: SessionDep):
    deleted = db.query(Event).delete()
    db.commit()
    return
