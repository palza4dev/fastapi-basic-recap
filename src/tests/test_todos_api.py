from database.orm import ToDo
from database.repository import ToDoRepository


def test_get_todos(client, mocker):
    # order=ASC
    mocker.patch.object(ToDoRepository, "get_todos", return_value=[
        ToDo(id=1, contents="Workout day 1", is_done=True),
        ToDo(id=2, contents="Workout day 2", is_done=False)
    ])
    response = client.get("/todos?")
    assert response.status_code == 200
    assert response.json() == {
        "todos":
            [
                {"id": 1, "contents": "Workout day 1", "is_done": True},
                {"id": 2, "contents": "Workout day 2", "is_done": False},
            ]
    }

    # order=DESC
    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "todos":
            [
                {"id": 2, "contents": "Workout day 2", "is_done": False},
                {"id": 1, "contents": "Workout day 1", "is_done": True},
            ]
    }


def test_get_todo(client, mocker):
    # 200
    mocker.patch.object(
        ToDoRepository, "get_todo_by_todo_id",
        return_value=ToDo(id=1, contents="todo", is_done=True),
    )
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "todo", "is_done": True}

    # 404
    mocker.patch.object(ToDoRepository, "get_todo_by_todo_id", return_value=None)
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo Not Found"}


def test_create_todo(client, mocker):
    # 201
    create_spy = mocker.spy(ToDo, "create")
    mocker.patch.object(
        ToDoRepository, "create_todo",
        return_value=ToDo(id=1, contents="todo", is_done=True),
    )
    body = {
        "contents": "test",
        "is_done": False
    }
    response = client.post("/todos", json=body)

    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done is False

    assert response.status_code == 201
    assert response.json() == {"id": 1, "contents": "todo", "is_done": True}


def test_update_todo(client, mocker):
    # 200
    mocker.patch.object(
        ToDoRepository, "get_todo_by_todo_id",
        return_value=ToDo(id=1, contents="todo", is_done=False),
    )
    done = mocker.patch.object(ToDo, "done")
    mocker.patch.object(
        ToDoRepository, "update_todo",
        return_value=ToDo(id=1, contents="todo", is_done=True),
    )
    response = client.patch("/todos/1", json={"is_done": True})

    done.assert_called_once_with()

    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "todo", "is_done": True}

    # 404
    mocker.patch.object(ToDoRepository, "get_todo_by_todo_id", return_value=None)

    response = client.patch("/todos/1", json={"is_done": True})
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo Not Found"}


def test_delete_todo(client, mocker):
    # 204
    mocker.patch.object(
       ToDoRepository, "get_todo_by_todo_id",
        return_value=ToDo(id=1, contents="todo", is_done=True),
    )
    mocker.patch.object(ToDoRepository, "delete_todo", return_value=None)

    response = client.delete("/todos/1")
    assert response.status_code == 204

    # 404
    mocker.patch.object(ToDoRepository, "get_todo_by_todo_id", return_value=None)
    response = client.delete("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo Not Found"}