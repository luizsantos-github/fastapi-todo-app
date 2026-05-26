from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    print(response.json)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'testadmin'

def test_change_password_success(test_user):
    response = client.put("/user/change_password", json={"old_password": "secret",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/change_password", json={"old_password": "wrong_password",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect password'}


def test_change_phone_number_success(test_user):
    response = client.put("/user/phone_number/2222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT
