from typing import List

from sqlalchemy.testing.schema import Table  # type: ignore

from src.user.db_tables import User

tables: List[Table] = [User]
