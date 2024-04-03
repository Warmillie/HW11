from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship, backref
from db import Base, engine


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    birthday = Column(Date)
    extra_data = Column(String, nullable=True)

# Створення таблиці в базі даних
Base.metadata.create_all(bind=engine)