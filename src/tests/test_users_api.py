from database.orm import User
from database.repository import UserRepository
from service.user import UserService


def test_user_sign_up(client, mocker):
    hash_password = mocker.patch.object(
        UserService, "hash_password", return_value="hashed"
    )
    user_create = mocker.patch.object(
        User, "create", return_value=User(id=None, username="test", password="hashed")
    )
    mocker.patch.object(
        UserRepository,
        "save_user",
        return_value=User(id=1, username="test", password="hashed"),
    )

    body = {"username": "test", "password": "plain"}
    response = client.post("/users/sign-up", json=body)

    hash_password.assert_called_once_with(plain_password="plain")
    user_create.assert_called_once_with(username="test", hashed_password="hashed")

    assert response.status_code == 201
    assert response.json() == {"id": 1, "username": "test"}


def test_user_log_in(client, mocker):
    get_user = mocker.patch.object(
        UserRepository,
        "get_user_by_username",
        return_value=User(id=1, username="test", password="hashed"),
    )
    verify = mocker.patch.object(UserService, "verify_password", return_value=True)
    create_jwt = mocker.patch.object(
        UserService, "create_jwt", return_value="jwt token"
    )

    body = {"username": "test", "password": "plain"}
    response = client.post("/users/log-in", json=body)

    get_user.assert_called_once_with(username="test")
    verify.assert_called_once_with(plain_password="plain", hashed_password="hashed")
    create_jwt.assert_called_once_with(username="test")

    assert response.status_code == 200
    assert response.json() == {"access_token": "jwt token"}
