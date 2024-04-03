from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: datetime
    extra_data: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True