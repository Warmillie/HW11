from datetime import date, timedelta
from typing import List, Optional

from roles import RoleAccess
from schemas import ContactCreate, ContactUpdate
from fastapi import FastAPI, Path, Query, Depends, HTTPException, status, Request, Security, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import text, or_
from db import get_db
import models
import schemas
import crud
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func
from passlib.context import CryptContext
import users
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
import auth_services
import auth

app = FastAPI()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_to_route_all = RoleAccess([models.Role.admin, models.Role.moderator])
app.include_router(auth.router, prefix="/api")
get_refresh_token = HTTPBearer()




@app.get('/')
def root():
    return {"message": "Application!"}

@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db),
                   current_user: models.User = Depends(auth_services.Auth.get_current_user)):
    try:
        return crud.create_contact(db=db, contact=contact)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Contact already exists")

@app.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(
    q: Optional[str] = None,
    db: Session = Depends(get_db), current_user: models.User = Depends(auth_services.Auth.get_current_user)
):
    return crud.get_contacts(db=db, q=q)

@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db),
                 current_user: models.User = Depends(auth_services.Auth.get_current_user)):
    db_contact = crud.get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db),
                   current_user: models.User = Depends(auth_services.Auth.get_current_user)):
    db_contact = crud.get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return crud.update_contact(db=db, contact_id=contact_id, contact=contact)

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(auth_services.Auth.get_current_user)):
    db_contact = crud.get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    crud.delete_contact(db=db, contact_id=contact_id)
    return {"message": "Contact deleted successfully"}

@app.get("/contacts/birthdays/", response_model=List[schemas.Contact])
def upcoming_birthdays(db: Session = Depends(get_db),
                       current_user: models.User = Depends(auth_services.Auth.get_current_user)):
    return crud.get_upcoming_birthdays(db=db)

