import pytest
from fastapi.testclient import TestClient
from main import app, tasks, task_id_counter
import itertools


@pytest.fixture
def client():
    # Reset state before each test
    tasks.clear()
    # Reset the counter by replacing it with a new one
    import main
    main.task_id_counter = itertools.count(1)
    return TestClient(app)


def test_create_task(client):
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "Test Description"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    assert "id" in data


def test_get_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks_with_data(client):
    # Create a task first
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_get_task_by_id(client):
    # Create a task
    create_response = client.post("/tasks", json={"title": "Task 1"})
    task_id = create_response.json()["id"]
    
    # Get the task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Task 1"


def test_get_task_not_found(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task_partial(client):
    # Create a task
    create_response = client.post("/tasks", json={
        "title": "Original Title",
        "description": "Original Description",
        "completed": False
    })
    task_id = create_response.json()["id"]
    
    # Update only the completed status
    response = client.patch(f"/tasks/{task_id}", json={"completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Original Title"
    assert data["description"] == "Original Description"
    assert data["completed"] is True


def test_update_task_full(client):
    # Create a task
    create_response = client.post("/tasks", json={"title": "Old Title"})
    task_id = create_response.json()["id"]
    
    # Update all fields
    response = client.patch(f"/tasks/{task_id}", json={
        "title": "New Title",
        "description": "New Description",
        "completed": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["description"] == "New Description"
    assert data["completed"] is True


def test_update_task_not_found(client):
    response = client.patch("/tasks/999", json={"completed": True})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task(client):
    # Create a task
    create_response = client.post("/tasks", json={"title": "Task to Delete"})
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/tasks/999")
    assert response.status_code == 404
