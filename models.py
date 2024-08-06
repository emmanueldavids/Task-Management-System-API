from sqlalchemy import Boolean, Column, Date, Integer, String
from database import Base
from datetime import date


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(50))
    


class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    description =Column(String(500))
    dueDate = Column(Date)
    status = Column(String(50))
    assigned_to = Column(Integer)
    user_id = Column(Integer)
    