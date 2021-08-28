from fastapi import Depends, APIRouter
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from src.blog.db_tables import BlogPost
from src.database import get_db
from src.user.db_tables import User
from src.user.functionality import get_current_user

router = APIRouter()


class CreateBlogRequest(BaseModel):
    content: str

    @validator('content')
    def content_should_not_be_empty(cls, value: str) -> str:
        if value == "":
            raise ValueError("content cannot be empty")
        return value


@router.post("/create-blog", tags=["blogs"])
async def create_blog(
    response: Response,
    create_blog_request: CreateBlogRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    response.status_code = status.HTTP_201_CREATED
    post = BlogPost(content=create_blog_request.content)
    db.add(post)
    db.commit()
    return {"detail": f"Successfully authenticated {current_user.username}"}
