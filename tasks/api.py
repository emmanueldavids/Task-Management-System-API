from enum import Enum
from msilib import schema
from fastapi import APIRouter, HTTPException, Response, Request, Depends,status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Annotated
import datetime
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

task_router = APIRouter()
models.Base.metadata.create_all(bind=engine)


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# Pydantic models
class TasksBase(BaseModel):
    title: str
    description: str
    dueDate: datetime.date
    status: TaskStatus
    assigned_to: int
    user_id: int

#dependency for the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


#----------START TASK API---------------

# Create task
@task_router.post("/", response_model=TasksBase)
async def create_task(task: TasksBase, db: db_dependency):
    db_task = models.Tasks(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db


# List all tasks
@task_router.get('/', response_model=List[TasksBase])
async def get_user(db: db_dependency):
    tasks = db.query(models.Tasks).all()
    if tasks is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    return tasks


# Get task by ID
@task_router.get('/tasks/{tasks_id}', status_code=status.HTTP_200_OK)
async def get_user(tasks_id: int,db: db_dependency):
    tasks = db.query(models.Tasks).filter(models.Tasks.id == tasks_id).first()
    if tasks is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    return tasks


# Get task by due date
@task_router.get("/tasks/due_date/{task_due_date}", status_code=status.HTTP_200_OK)
async def task_due_date(tasks_due_date: datetime.date, db: db_dependency):
    filtered_tasks = db.query(models.Tasks).filter(models.Tasks.id == tasks_due_date).first()
    if not filtered_tasks:
        raise HTTPException(status_code=404, detail="No Due Date found for the specified due date")
    return filtered_tasks


# Update task
@task_router.put('/tasks/{task_id}', status_code=status.HTTP_200_OK)
async def update_task(task_id: int, task: TasksBase, db: db_dependency):
    update_task = db.query(models.Tasks).filter((models.Tasks.id) == task_id).first()
    if update_task is None:
        raise HTTPException(status_code=404, detail='Task Not Found')
    
    update_task.title = task.title
    update_task.description = task.description
    
    db.commit()
    return update_task


# to Delete tasks by id
@task_router.delete('/tasks/{task_id}', status_code=status.HTTP_200_OK)
async def get_task(task_id: int, db: db_dependency):
    task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    db.delete(task)
    db.commit()
    return "Task Deleted Successfull"

#------------------END OF TASK API------------------------------------------

#-----------------TASK ASSIGNMENT API---------------------------------------

# Assign task to user using user_id
@task_router.post("/tasks/{task_id}/assign", status_code=status.HTTP_201_CREATED)
async def assign_task(task_id: int, user_id: int, db: db_dependency):
    task = db.query(models.Tasks).filter((models.Tasks.id) == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.assigned_to = user_id
    db.commit()
    # send_notification(user_id, f"Task Assigned: {task.title}")
    return task

@task_router.get("/{task_id}", status_code=status.HTTP_200_OK)
async def get_assigned_task(task_id: int, db: db_dependency):
    task = db.query(models.Tasks).filter((models.Tasks) == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Print task details
    print(f"User ID: {task.assigned_to}")
    print(f"Task Title: {task.title}")
    print(f"Task Description: {task.description}")
    print(f"Due Date: {task.due_date}")
    
    return task
