import pytest
from fastapi.testclient import TestClient
from main import app, tasks, next_id

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_tasks():
    """Reset the tasks dictionary and next_id before each test."""
    tasks.clear()
    import main
    main.next_id = 1
    yield


def test_create_task():
    """Test creating a new task."""
    response = client.post(
        "/tasks",
        json={"title": "Test Task", "description": "Test Description", "completed": False}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False


def test_get_all_tasks():
    """Test getting all tasks."""
    # Create a couple of tasks first
    client.post("/tasks", json={"title": "Task 1", "description": "First task"})
    client.post("/tasks", json={"title": "Task 2", "description": "Second task"})
    
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_get_task_by_id():
    """Test getting a specific task by ID."""
    # Create a task first
    create_response = client.post(
        "/tasks",
        json={"title": "Specific Task", "description": "Get this one"}
    )
    task_id = create_response.json()["id"]
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Specific Task"
    assert data["description"] == "Get this one"


def test_get_task_not_found():
    """Test getting a non-existent task returns 404."""
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task():
    """Test deleting a task."""
    # Create a task first
    create_response = client.post(
        "/tasks",
        json={"title": "Task to Delete", "description": "Will be deleted"}
    )
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found():
    """Test deleting a non-existent task returns 404."""
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
