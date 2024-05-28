from datetime import datetime

from pydantic import BaseModel, PositiveInt


class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]


external_data = {
    "id": 123,
    "name": "Alice",
    "signup_ts": datetime.now(),
    "tastes": {"chocolate": 5, "vanilla": 3},
}

user = User(**external_data)

print(user.model_dump())

"""
{
    "id": 123,
    "name": "Alice",
    "signup_ts": datetime.datetime(2024, 5, 16, 2, 57, 14, 67759),
    "tastes": {"chocolate": 5, "vanilla": 3},
}
"""

print(user.json())

"""
{
    "id": 123,
    "name": "Alice",
    "signup_ts": "2024-05-16T03:48:04.746758",
    "tastes": {"chocolate": 5, "vanilla": 3},
}
"""
