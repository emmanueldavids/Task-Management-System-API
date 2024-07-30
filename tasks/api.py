from enum import Enum
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import datetime
import smtplib
from email.mime.text import MIMEText
from users.api import users

task_router = APIRouter()

tasks = []

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# Pydantic models
class Task(BaseModel):
    id: int
    title: str
    description: str
    dueDate: datetime.date
    status: TaskStatus
    assigned_to: int
    user_id: int

class TaskIn(BaseModel):
    title: str
    description: str
    dueDate: datetime.datetime
    user_id: int



# tasks.status = TaskStatus.COMPLETED

# TASK API
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
async def read_task_by_due_date(task_due_date: datetime.date):
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

# to Delete tasks by id
@task_router.delete("/{task_id}")
async def delete_task(task_id: int):
    for i, t in enumerate(tasks):
        if t.id == task_id:
            del tasks[i]
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")

#------------------END OF TASK API------------------------------------------

#-----------------TASK ASSIGNMENT API---------------------------------------
#Sending Notification for task 
# def send_notification(user_id: int, message: str):
#       # Find the user by ID and get their email
#     user = next((user for user in users if (user.id) == user_id), None)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Replace with your email credentials
#     sender_email = "emmanueldavids417@gmail.com"
#     sender_password = "Solateck=5"
    
#     # Replace with the user's email
#     receiver_email = user.email
    
#     # Create the email message
#     msg = MIMEText(message)
#     msg['Subject'] = "Task Notification"
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
    
#     # Send the email using SMTP
#     server = smtplib.SMTP('(smtp.gmail.com)', 587)
#     server.starttls()
#     server.login(sender_email, sender_password)
#     server.sendmail(sender_email, receiver_email, msg.as_string())
#     server.quit()

# Assign task to user using user_id
@task_router.post("/{task_id}/assign")
async def assign_task(task_id: int, user_id: int):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.assigned_to = user_id
    # send_notification(user_id, f"Task Assigned: {task.title}")
    return task

# Send reminder to user
# async def send_due_date_reminder(task: Task):
#     send_notification(task.assigned_to, f"Reminder: {task.title} due on {task.due_date}")

# Schedule reminder for each task
# for task in tasks:
#     if task.due_date - datetime.now() <= datetime.timedelta(days=1):
#         send_due_date_reminder(task)



# will Get tasks assigned to a user
@task_router.get("/user", response_model=List[Task])
async def get_user_tasks(user_id: int):
    user_tasks = [task for task in tasks if task.assigned_to == user_id]
    if not user_tasks:
        raise HTTPException(status_code=404, detail="No tasks found for the specified user")
    return user_tasks



# #post completed task
# @task_router.post("/tasks/{task_id}/complete")
# async def complete_task(task_id: int):
#     for task in tasks:
#         if (task.id) == task_id:
#             task.status = TaskStatus.COMPLETED
#             # Send notification to user
#             send_notification(task.assigned_to, f"Task completed: {task.title}")
#             return task
#     raise HTTPException(status_code=404, detail="Task not found")
