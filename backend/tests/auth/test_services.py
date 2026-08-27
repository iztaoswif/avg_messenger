import pytest
from app.core.passwords import is_password_correct
from app.repositories.users import select_user_by_username
from app.auth.services import register_user, login_user
from app.auth.exceptions import UsernameTakenError, InvalidCredentialsError
from sqlalchemy.ext.asyncio import AsyncConnection


async def test_register_service_creates_user(conn: AsyncConnection):
    await register_user(conn, "testuser", "password123")

    user = await select_user_by_username(conn, "testuser")
    assert user is not None
    assert user["username"] == "testuser"


async def test_register_service_is_hashes_password(conn: AsyncConnection):
    await register_user(conn, "testuser", "password123")

    user = await select_user_by_username(conn, "testuser")
    password_hash = user["password_hash"]
    assert password_hash != "password123"
    assert await is_password_correct(password_hash, "password123")


async def test_register_service_duplicate_raises(conn: AsyncConnection):
    await register_user(conn, "testuser", "password123")
    with pytest.raises(UsernameTakenError):
        await register_user(conn, "testuser", "password123")


async def test_login_service_invalid_credentials_raises(conn: AsyncConnection):
    with pytest.raises(InvalidCredentialsError):
        await login_user(conn, "nonexistent", "password123")
