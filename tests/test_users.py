from jose import jwt
from app import schemas, config
import pytest


def test_create_user(client):
    response = client.post("/users", json={"email":"hello@gmail.com", "password":"test1234"})
    new_user = schemas.UserResponse(**response.json())
    assert response.status_code == 201
    assert new_user.email == "hello@gmail.com"

def test_login_user(test_user, client):
    response = client.post("/login", data={"username":test_user["email"], "password":test_user["password"]})
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("username, password, status", [("hello@mail.com", None, 422), 
                                                        (None, "test1234", 422), 
                                                        ("hello@gmail.com", "wrongpass", 403)])
def test_inncorect_user(client, username, password, status):
    response = client.post("/login", data={"username":username, "password":password})
    assert response.status_code == status