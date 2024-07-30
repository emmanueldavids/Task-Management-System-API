# Task-Management-System
Task Management System using Python FastAPI.
Overview

This project is a RESTful API for managing tasks. It allows signup, Login and also allows users to create, read, update, and delete tasks.

Features
- Signup/Login 
- Create new tasks
- Retrieve a list of all tasks
- Retrieve a single task by ID
- Update existing tasks
- Delete tasks
- Assign task to a user
  

Endpoints
- GET / : Retrieve users
- POST /: Create a new user
- GET /tasks: Retrieve a list of all tasks
- POST /tasks: Create a new task
- GET /tasks/{task_id}: Retrieve a single task by ID
- PUT /tasks/{task_id}: Update an existing task
- DELETE /tasks/{task_id}: Delete a task
- POST /{task_id}/assign: Assign task to a user


Requirements

- Python 3.8+
- FastAPI
- Pydantic


Setup

1. Clone the repository
2. Install dependencies: pip install -r requirements.txt
3. Run the API: python -m uvicorn main:app --reload => For Windows
4. Run the API: uvicorn main:app --reload => For Linux


Contributing

Contributions are welcome! Please submit a pull request with your changes.
