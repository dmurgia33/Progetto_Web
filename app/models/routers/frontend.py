from fastapi import APIRouter, Request, Depends, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import config
from app.data.db import SessionDep
from app.models.event import Event, EventRead  # Ho aggiunto EventCreate che mancava
from sqlmodel import select, Session,delete
from typing import List, Annotated
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


