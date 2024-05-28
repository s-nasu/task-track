from fastapi import status

from tests.factories.todo import TodoFactory
from tests.factories.user import UserFactory


def test_create_user(auth_headers, client, db_session):
    response = client.post(
        "/api/v1/users",
        json={"name": "John Doe", "email": "john.doe@example.com"},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john.doe@example.com"


def test_read_users(client, db_session):
    cnt = 5
    users = [UserFactory() for _ in range(cnt)]

    for user in users:
        for _ in range(cnt):
            todo = TodoFactory(assignee=None, creator=user, updater=user)
            user.assigned_todos.append(todo)

    db_session.add_all(users)
    db_session.commit()
    response = client.get("/api/v1/users")

    users_data = response.json()

    assert response.status_code == status.HTTP_200_OK

    for user in users_data:
        len(user["assigned_todos"]) == cnt
    assert len(users_data) == cnt


def test_read_user(client, db_session):
    user = UserFactory()
    cnt = 5
    for _ in range(cnt):
        todo = TodoFactory(assignee=None)
        user.assigned_todos.append(todo)
    db_session.commit()
    response = client.get(f"/api/v1/users/{user.id}")

    user_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(user_data["assigned_todos"]) == cnt
    assert user_data["name"] == user.name
    assert user_data["email"] == user.email
    assert user_data["id"] == str(user.id)


def test_update_user(client, db_session):
    user = UserFactory()
    db_session.add(user)
    db_session.commit()

    user_data = {"name": "Updated Name", "email": "updated.email@example.com"}

    response = client.patch(f"/api/v1/users/{user.id}", json=user_data)

    assert user.name == user_data["name"]
    assert user.email == user_data["email"]
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_user(client, db_session):
    user = UserFactory()
    db_session.add(user)
    db_session.commit()
    response = client.delete(f"/api/v1/users/{user.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_user_todos(client, db_session):
    user = UserFactory()
    cnt = 5
    for _ in range(cnt):
        TodoFactory(assignee=user)

    response = client.get(f"/api/v1/users/{user.id}/todos")
    assert response.status_code == status.HTTP_200_OK
    todos = response.json()

    assert len(todos) == cnt  # 作成したTodoの数と一致することを確認
    # for todo in todos:
    #     assert todo["assignee_id"] == str(
    #         user.id
    #     )  # Todoが正しいユーザーに割り当てられていることを確認
