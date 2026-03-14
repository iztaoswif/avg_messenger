from asyncio import to_thread
from argon2 import PasswordHasher

ph = PasswordHasher()

async def get_password_hash(password: str) -> str:
    return await to_thread(ph.hash, password)


async def is_password_correct(
    password_hash: str,
    plain_password: str) -> bool:

    try:
        return await to_thread(ph.verify, password_hash, plain_password)
    except Exception:
        return False