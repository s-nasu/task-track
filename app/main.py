from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from dependencies.authorization import verify_token
from routers import models, todos, users
from routers.admin import users as admin_users

app = FastAPI(
    title="カンバンタスク管理アプリケーション",
    description="カンバンタスク管理アプリケーションは、タスクの管理とユーザーの管理を行うアプリケーションです。",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    summary="This is a Kanban task management application.",
    contact={
        "name": "デッドプール",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=[
        {
            "name": "users",
            "description": "**ユーザー管理**に関する操作。",
            "externalDocs": {
                "description": "ユーザー管理に関するドキュメント",
                "url": "https://example.com/users",
            },
        },
        {
            "name": "todos",
            "description": "**タスク管理**に関する操作。",
        },
        {
            "name": "models",
            "description": "テスト用のエンドポイント。",
        },
    ],
    dependencies=[Depends(verify_token)],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_domains,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


for router in [todos.router, users.router, models.router]:
    app.include_router(
        router,
        prefix="/api/v1",
    )

admin_api = FastAPI(
    title="管理者用API",
    description="管理者用APIは、管理者のみがアクセスできるエンドポイントを提供します。",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    summary="This is an API for administrators.",
    contact={
        "name": "デッドプール",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=[
        {
            "name": "users",
            "description": "**ユーザー管理**に関する操作。",
        },
    ],
    # servers=[
    #     {"url": "/docs", "description": "顧客用"},
    # ],
    # dependencies=[Depends(verify_token)],
)

admin_api.include_router(
    admin_users.router,
    # prefix="/api/v1",
)

app.mount("/admin", admin_api)
