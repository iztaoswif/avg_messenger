from sqlalchemy import (insert,
select,
exists)

from app.db.engine import engine
from app.db.models import users


def is_username_taken(username: str) -> bool:
    stmt = select(exists().where(users.c.username == username))

    with engine.connect() as conn:
        return conn.execute(stmt).scalar()


def create_user(username: str, password_hash: str) -> None:
    stmt = insert(users).values(username=username,
        password_hash=password_hash)

    with engine.begin() as conn:
        conn.execute(stmt)


def get_user_by_username(username: str):
    stmt = select(users).where(users.c.username == username).limit(1)
    with engine.connect() as conn:
        return conn.execute(stmt).mappings().first()


def get_user_by_id(id: int):
    stmt = select(users).where(users.c.id == id).limit(1)
    with engine.connect() as conn:
        return conn.execute(stmt).mappings().first()
