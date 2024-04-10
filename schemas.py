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


# Схема для створення нового користувача (реєстрація)
class UserCreate(BaseModel):
    email: str
    password: str

# Схема для входу користувача (автентифікація)
class UserLogin(BaseModel):
    email: str
    password: str

# Модель користувача в базі даних
class User(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True
