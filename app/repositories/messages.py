from sqlalchemy import (insert,
select)

from app.db.engine import engine
from app.db.models import messages, users



def create_message(sender_id: int, content: str) -> None:
    stmt = insert(messages).values(sender_id=sender_id,
        content=content)

    with engine.begin() as conn:
        conn.execute(stmt)


def fetch_messages(after_id: int):
    stmt = (
        select(
            messages.c.id,
            messages.c.sender_id,
            messages.c.content,
            messages.c.created_at,
            users.c.username.label("sender_username")
        )
        .join(users, messages.c.sender_id == users.c.id)
        .where(messages.c.id > after_id)
        .order_by(messages.c.id.asc())
    )

    with engine.connect() as conn:
        return [
            {
                "id": row.id,
                "sender_id": row.sender_id,
                "sender_username": row.sender_username,
                "content": row.content,
                "created_at": row.created_at.isoformat()
            }

            for row in conn.execute(stmt).mappings()
        ]


def fetch_messages_iter(after_id: int):
    stmt = select(messages).where(messages.c.id > after_id)
    with engine.connect() as conn:
        yield from conn.execute(stmt).mappings()

