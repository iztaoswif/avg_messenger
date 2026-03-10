from sqlalchemy import (MetaData,
Text,
DateTime,
func,
Table,
Column,
Integer,
String,
ForeignKey)


metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column(
        "id",
        Integer, primary_key=True),
    Column(
        "username",
        Text,
        nullable=False,
        unique=True,
        index=True),
    Column(
        "password_hash",
        String,
        nullable=False)
)


messages = Table(
    "messages",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True),
    Column(
        "sender_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True),
    Column(
        "content",
        Text,
        nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False)
)
