from fastapi import Depends, APIRouter
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response

from src.user.db_tables import User
from src.user.functionality import get_current_user

router = APIRouter()


class CreateBlogRequest(BaseModel):
    content: str


@router.post("/create-blog", tags=["blogs"])
async def create_blog(
    response: Response,
    create_blog_request: CreateBlogRequest,
    current_user: User = Depends(get_current_user),
) -> dict:
    response.status_code = status.HTTP_201_CREATED
    return {"detail": f"Successfully authenticated {current_user.username}"}
