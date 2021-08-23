from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.users.http_endpoints import router as users_router
from src.file_management.http_endpoints import router as file_management_router

app = FastAPI()

app.include_router(users_router)
app.include_router(file_management_router)

app.mount(
    "/ui",
    StaticFiles(directory=str((Path(".") / "src" / "static").absolute())),
    name="static",
)


@app.get("/")
async def index_endpoint() -> dict:
    return {"msg": "Hey"}
