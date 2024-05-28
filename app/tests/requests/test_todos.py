from itertools import cycle

from fastapi import status
from sqlmodel import func, select

from models.todo import TaskStatus, Todo
from tests.factories.todo import TodoFactory


def test_read_todos(client, db_session):
    # テスト用のTodoを作成します
    cnt = 10
    statuses = cycle(TaskStatus)
    todos = [TodoFactory(status=next(statuses)) for _ in range(cnt)]
    db_session.add_all(todos)
    db_session.commit()

    # デフォルトのクエリパラメータでテストします
    response = client.get("/api/v1/todos")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == cnt

    # カスタムのクエリパラメータでテストします
    response = client.get("/api/v1/todos?offset=0&limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2

    filter_status = 1

    response = client.get(f"/api/v1/todos?offset=0&limit=10&status={filter_status}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    count_statement = (
        select(func.count()).select_from(Todo).where(Todo.status == filter_status)
    )
    total = db_session.exec(count_statement).one()

    assert len(data) == total

    for item in data:
        assert item["status"] == filter_status


def test_read_todo(client, db_session):
    # テスト用のTodoを作成します
    todo = TodoFactory()
    db_session.add(todo)
    db_session.commit()

    # テスト用のTodoを取得します
    response = client.get(f"/api/v1/todos/{todo.id}")

    # レスポンスのステータスコードをチェックします
    assert response.status_code == status.HTTP_200_OK

    # レスポンスのデータをチェックします
    data = response.json()
    assert "id" in data
    assert data["id"] == str(todo.id)
    assert data["title"] == todo.title
    assert data["description"] == todo.description
    assert data["status"] == todo.status.value


def test_create_todo(client):
    # テストデータを作成します
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    response = client.post("/api/v1/todos", json=todo_data)

    # レスポンスのステータスコードとデータを検証します
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["title"] == todo_data["title"]
    assert data["description"] == todo_data["description"]
    assert data["status"] == 1


def test_update_todo(client, db_session):
    # テスト用のTodoを作成します
    todo = TodoFactory()
    db_session.add(todo)
    db_session.commit()

    # テスト用のTodoを更新します
    updated_todo_data = {
        "title": "Updated Todo",
        "description": "This is an updated todo",
        "status": 1,
    }
    response = client.patch(f"/api/v1/todos/{todo.id}", json=updated_todo_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # データベース内のTodoが更新されたかをチェックします
    updated_todo = db_session.get(Todo, todo.id)
    assert updated_todo.title == updated_todo_data["title"]
    assert updated_todo.description == updated_todo_data["description"]
    assert updated_todo.status.value == updated_todo_data["status"]


def test_delete_todo(client, db_session):
    # テスト用のTodoを作成します
    todo = TodoFactory()
    db_session.add(todo)
    db_session.commit()

    # テスト用のTodoを削除します
    response = client.delete(f"/api/v1/todos/{todo.id}")

    # レスポンスのステータスコードをチェックします
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # データベースからTodoが削除されたかをチェックします
    deleted_todo = db_session.get(Todo, todo.id)
    assert deleted_todo is None
