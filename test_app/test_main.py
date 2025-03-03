from fastapi.testclient import TestClient

from myapp.main import app

client = TestClient(app)


def test_get_user():
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_get_post_del_user():
    user = {"first_name": "Ivanov", "last_name": "Ivan", "email": "user@example.com", "age": 15}
    response = client.post("/users/add/", json=user)
    assert response.status_code == 200
    assert response.json() == {"message": "User Ivanov Ivan with email user@example.com added"}


def test_del_user():
    user = {"first_name": "Ivanov", "last_name": "Ivan", "email": "user@example.com", "age": 15}
    response = client.request("DELETE", "/users/del/", json=user)
    assert response.status_code == 200
    assert response.json() == {"message": "User Ivanov Ivan with email user@example.com deleted"}
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == {'users': []}