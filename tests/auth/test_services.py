import pytest
from app.core.passwords import is_password_correct
from app.repositories.users import get_user_by_username
from app.auth.services import register_user, login_user
from app.auth.exceptions import UsernameTakenError, InvalidCredentialsError
from sqlalchemy.ext.asyncio import AsyncSession


async def test_register_service_creates_user(session: AsyncSession):
    await register_user(session, "testuser", "password123")

    user = await get_user_by_username(session, "testuser")
    assert user is not None
    assert user["username"] == "testuser"


async def test_register_service_is_hashes_password(session: AsyncSession):
    await register_user(session, "testuser", "password123")

    user = await get_user_by_username(session, "testuser")
    password_hash = user["password_hash"]
    assert password_hash != "password123"
    assert await is_password_correct(password_hash, "password123")


async def test_register_service_duplicate_raises(session: AsyncSession):
    await register_user(session, "testuser", "password123")
    with pytest.raises(UsernameTakenError):
        await register_user(session, "testuser", "password123")


async def test_login_service_invalid_credentials_raises(session: AsyncSession):
    with pytest.raises(InvalidCredentialsError):
        await login_user(session, "nonexistent", "password123")
