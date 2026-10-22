from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Task List API")

# In-memory storage
tasks = {}
next_id = 1


class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskResponse(Task):
    id: int


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: Task):
    """Create a new task."""
    global next_id
    task_id = next_id
    next_id += 1
    
    task_data = task.dict()
    task_data["id"] = task_id
    tasks[task_id] = task_data
    
    return task_data


@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    """Get all tasks."""
    return list(tasks.values())


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """Get a specific task by ID."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task by ID."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return None
