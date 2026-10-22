from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import itertools

app = FastAPI()

# In-memory storage
tasks = {}
# Thread-safe ID generator
task_id_counter = itertools.count(1)


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False


@app.post("/tasks", status_code=201, response_model=Task)
def create_task(task: TaskCreate):
    task_id = next(task_id_counter)
    new_task = Task(
        id=task_id,
        title=task.title,
        description=task.description,
        completed=task.completed
    )
    tasks[task_id] = new_task
    return new_task


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return list(tasks.values())


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    update_data = task_update.model_dump(exclude_unset=True)
    
    updated_task = task.model_copy(update=update_data)
    tasks[task_id] = updated_task
    
    return updated_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
