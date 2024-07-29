from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import datetime

task_router = APIRouter()

tasks = []

# Pydantic models
class Task(BaseModel):
    id: int
    title: str
    description: str
    dueDate: datetime.datetime
    status: str
    assigned_to: int
    user_id: int

class TaskIn(BaseModel):
    title: str
    description: str
    dueDate: datetime.datetime
    user_id: int

# Create task
@task_router.post("/", response_model=Task)
async def create_task(task: Task):
    tasks.append(task)
    return task

# List all tasks
@task_router.get("/", response_model=List[Task])
async def read_tasks():
    return tasks

# Get task by ID
@task_router.get("/{task_id}", response_model=Task)
async def read_task(task_id: int):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Get task by due date
@task_router.get("/due_date/{task_due_date}", response_model=List[Task])
async def read_task_by_due_date(task_due_date: datetime.datetime):
    filtered_tasks = [task for task in tasks if task.dueDate == task_due_date]
    if not filtered_tasks:
        raise HTTPException(status_code=404, detail="No tasks found for the specified due date")
    return filtered_tasks

# Update task
@task_router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    for i, t in enumerate(tasks):
        if t.id == task_id:
            tasks[i] = task
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# Delete task
@task_router.delete("/{task_id}")
async def delete_task(task_id: int):
    for i, t in enumerate(tasks):
        if t.id == task_id:
            del tasks[i]
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")

# Assign task to user
@task_router.post("/{task_id}/assign")
async def assign_task(task_id: int, user_id: int):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.assigned_to = user_id
    return task

# Get tasks assigned to a user
@task_router.get("/user", response_model=List[Task])
async def get_user_tasks(user_id: int):
    user_tasks = [task for task in tasks if task.assigned_to == user_id]
    if not user_tasks:
        raise HTTPException(status_code=404, detail="No tasks found for the specified user")
    return user_tasks

#Get all task assigned to a user
@task_router.get("/", response_model=List[Task])
async def get_all_tasks():
    return tasks