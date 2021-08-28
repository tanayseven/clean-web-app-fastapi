import uuid

from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base


class BlogPost(Base):
    __tablename__ = "blog_post"
    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(Text, nullable=False)
