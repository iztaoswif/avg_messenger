from sqlalchemy import (
    MetaData,
    DateTime,
    func,
    Table,
    Column,
    Integer,
    String,
    ForeignKey
)


metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True
    ),
    Column(
        "username",
        String(30),
        nullable=False,
        unique=True,
        index=True
    ),
    Column(
        "password_hash",
        String(200),
        nullable=False
    )
)


messages = Table(
    "messages",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True
    ),
    Column(
        "sender_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    ),
    Column(
        "chat_id",
        Integer,
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False
        #, index=True
    ),
    Column(
        "content",
        String(1024),
        nullable=False
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
)


chats = Table(
    "chats",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True
    ),
    Column(
        "name",
        String(80),
        nullable=False
        #, index=True
    )
)


chat_members = Table(
    "chat_members",
    metadata,
    Column(
        "chat_id",
        Integer,
        ForeignKey("chats.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
)
