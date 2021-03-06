from sqlalchemy.orm import Session

from src.user.db_tables import User
from src.user.functionality import hash_password


def create_john_doe_user(db: Session) -> None:
    user = User(
        username="john.doe",
        password=hash_password("password"),
        email="john.doe@company.com",
    )
    db.add(user)
    db.commit()
