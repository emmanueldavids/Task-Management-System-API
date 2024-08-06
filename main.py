from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from users.api import user_router
from tasks.api import task_router


app = FastAPI(
    title="Task Management System fastAPI",
    description="This is the main app that includes all the APIs",
    version="1.0",
)

template = Jinja2Templates(directory="templates")

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])

