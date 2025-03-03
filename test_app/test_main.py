from fastapi.testclient import TestClient

from myapp.main import app

client = TestClient(app)


def test_get_user():
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_post_user():
    user = {"first_name": "Ivan", "last_name": "Ivanov", "email": "user@example.com", "age": 15}
    response = client.post("/users/add/", json=user)
    assert response.status_code == 200
    assert response.json() == {"message": "User Ivan Ivanov with email user@example.com added"}


def test_del_user():
    user = {"first_name": "Ivan", "last_name": "Ivanov", "email": "user@example.com", "age": 15}
    response = client.request("DELETE", "/users/del/", json=user)
    assert response.status_code == 200
    assert response.json() == {"message": "User Ivan Ivanov with email user@example.com deleted"}
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == {'users': []}

def test_fail_post_user():
    user = {"first_name": "I", "last_name": "Ivanov", "email": "user@example.com", "age": 15}
    response = client.post("/users/add/", json=user)
    assert response.status_code == 422
    assert (response.json()["detail"][0]["msg"]) == 'String should have at least 2 characters'
    user = {"first_name": "Ivan", "last_name": "I", "email": "user@example.com", "age": 15}
    response = client.post("/users/add/", json=user)
    assert response.status_code == 422
    assert (response.json()["detail"][0]["msg"]) == 'String should have at least 2 characters'
    user = {"first_name": "Ivan", "last_name": "Ivanov", "email": "user@examplecom", "age": 15}
    response = client.post("/users/add/", json=user)
    assert response.status_code == 422
    assert (response.json()["detail"][0]["msg"]) == 'value is not a valid email address: The part after the @-sign is not valid. It should have a period.'
    user = {"first_name": "Ivan", "last_name": "Ivanov", "email": "user@example.com", "age": 1}
    response = client.post("/users/add/", json=user)
    assert response.status_code == 422
    assert (response.json()["detail"][0]["msg"]) == 'Input should be greater than or equal to 10'
