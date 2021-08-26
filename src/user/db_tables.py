import uuid

from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
