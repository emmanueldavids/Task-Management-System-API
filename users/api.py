from fastapi import APIRouter, HTTPException, Response, Request, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import models
from typing import List, Annotated
from database import engine, SessionLocal
from sqlalchemy.orm import Session

user_router = APIRouter()
models.Base.metadata.create_all(bind=engine)

# Pydantic models
class UserBase(BaseModel):
    username: str
    email: str
    password: str

# class UserInBase(BaseModel):
#     username: str
#     email: str
#     password: str

# class UserOutBase(BaseModel):
#     id: int
#     username: str
#     email: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# OAuth2 password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#Post user (Create User)
@user_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    new_user = models.User(username=user.username, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    return new_user

#Get all user
@user_router.get("/", status_code=status.HTTP_200_OK)
async def read_users(db: db_dependency):
    users = db.query(models.User).all()
    return users

#Get user by id
@user_router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter((models.User.id) == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Post Users Login
@user_router.post("/token", status_code=status.HTTP_201_CREATED)
async def login( db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": user.username, "token_type": "bearer"}

# Update User
@user_router.put('/{user_id}', status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserBase, db: db_dependency):
    update_user = db.query(models.User).filter((models.User.id) == user_id).first()
    if update_user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    
    update_user.title = user.title
    update_user.description = user.description
    
    db.commit()
    return update_user

# to Delete Users by id
@user_router.delete('/{user_id}', status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    db.delete(user)
    db.commit()
    return "User Deleted Successfull"

