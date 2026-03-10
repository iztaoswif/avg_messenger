from sqlalchemy import (insert,
select)

from app.db.engine import engine
from app.db.models import messages
from app.repositories.users import get_user_by_id



def create_message(sender_id: int, content: str) -> None:
    stmt = insert(messages).values(sender_id=sender_id,
        content=content)

    with engine.begin() as conn:
        conn.execute(stmt)


def fetch_messages(after_id: int):
    stmt = select(messages).where(messages.c.id > after_id).order_by(messages.c.id.asc())

    result = []
    with engine.connect() as conn:
        for row in conn.execute(stmt).mappings():
            user = get_user_by_id(row["sender_id"])
            result.append({
                "id": row["id"],
                "sender_id": row["sender_id"],
                "sender_username": user["username"] if user else "unknown",
                "content": row["content"],
                "created_at": row["created_at"].isoformat()
            })

    return result


def fetch_messages_iter(after_id: int):
    stmt = select(messages).where(messages.c.id > after_id)
    with engine.connect() as conn:
        yield from conn.execute(stmt).mappings()

