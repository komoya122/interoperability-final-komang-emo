# schemas.py
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class EventBase(BaseModel):
    title: str
    date: date
    location: Optional[str] = None
    quota: int

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str]
    date: Optional[date]
    location: Optional[str]
    quota: Optional[int]

class EventOut(EventBase):
    id: int
    class Config:
        orm_mode = True

class ParticipantCreate(BaseModel):
    name: str
    email: EmailStr
    event_id: int

class ParticipantOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    event_id: int
    class Config:
        orm_mode = True
