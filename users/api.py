from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List

user_router = APIRouter()

# Pydantic models
class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

class UserIn(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str

# will replace with a real database
users = []

# OAuth2 password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create user
@user_router.post("/", response_model=UserOut)
async def create_user(user: UserIn):
    new_user = User(id=len(users) + 1, username=user.username, email=user.email, password=user.password)
    users.append(new_user)
    return new_user

# List all users
@user_router.get("/", response_model=List[UserOut])
async def read_users():
    return users

# Get user by ID
@user_router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Token endpoint
@user_router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = next((user for user in users if user.username == form_data.username), None)
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": user.username, "token_type": "bearer"}
