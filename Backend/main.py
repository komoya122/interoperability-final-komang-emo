# main.py
from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, database
from fastapi.middleware.cors import CORSMiddleware

# Admin token sederhana (bonus)
ADMIN_TOKEN = "secret-admin-token"

app = FastAPI(title="Campus Event Registration API")

# CORS - agar frontend static dapat akses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # di produksi batasi origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB (tables)
models.Base.metadata.create_all(bind=database.engine)

# Dependency: DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Event endpoints ---
@app.get("/events", response_model=List[schemas.EventOut])
def read_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()

@app.post("/events", response_model=schemas.EventOut)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db), x_admin_token: Optional[str] = Header(None)):
    # simple auth: require header "x-admin-token" == ADMIN_TOKEN
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.put("/events/{event_id}", response_model=schemas.EventOut)
def update_event(event_id: int, event: schemas.EventUpdate, db: Session = Depends(get_db), x_admin_token: Optional[str] = Header(None)):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(404, "Event not found")
    for field, value in event.dict(exclude_unset=True).items():
        setattr(db_event, field, value)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db), x_admin_token: Optional[str] = Header(None)):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(404, "Event not found")
    db.delete(db_event)
    db.commit()
    return {"detail": "Event deleted"}

# --- Participants / Registration ---
@app.post("/register", response_model=schemas.ParticipantOut)
def register_participant(p: schemas.ParticipantCreate, db: Session = Depends(get_db)):
    # Validate event exists and quota not exceeded
    event = db.query(models.Event).filter(models.Event.id == p.event_id).first()
    if not event:
        raise HTTPException(404, "Event not found")
    # count participants
    current_count = db.query(models.Participant).filter(models.Participant.event_id == p.event_id).count()
    if current_count >= event.quota:
        raise HTTPException(400, "Event quota full")
    participant = models.Participant(**p.dict())
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant

@app.get("/participants", response_model=List[schemas.ParticipantOut])
def list_participants(db: Session = Depends(get_db)):
    return db.query(models.Participant).all()
