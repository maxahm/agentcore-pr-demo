# Task List API

A simple FastAPI-based task list application with in-memory storage.

## Features

- Create tasks (POST /tasks)
- List all tasks (GET /tasks)
- Get a specific task (GET /tasks/{id})
- Delete a task (DELETE /tasks/{id})

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

API documentation (Swagger UI) available at http://localhost:8000/docs

## Running Tests

```bash
pytest test_main.py -v
```

## API Endpoints

### Create a Task
```
POST /tasks
Content-Type: application/json

{
  "title": "My Task",
  "description": "Task description",
  "completed": false
}
```

### Get All Tasks
```
GET /tasks
```

### Get a Specific Task
```
GET /tasks/{task_id}
```

### Delete a Task
```
DELETE /tasks/{task_id}
```
