# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from users.api import users_router
# # from tasks.api import tasks_router
# # from auth.api import auth_router

# app = FastAPI(
#     title="Main App",
#     description="This is the main app that includes all the APIs",
#     version="1.0",
#     openapi_tags=[
#         {"name": "users", "description": "User management"},
#         # {"name": "tasks", "description": "Task management"},
#         # {"name": "auth", "description": "Authentication"},
#     ]
# )

# # app.include_router(users_router, prefix="/users", tags=["users"])
# # app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
# # app.include_router(auth_router, prefix="/auth", tags=["auth"])


from fastapi import FastAPI
from users.api import user_router
from tasks.api import task_router

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Task Management System"}

# Note: Do not include `if __name__ == "__main__":` block here. Use uvicorn command to run the app.

# Run the application with:
# uvicorn main:app --reload
