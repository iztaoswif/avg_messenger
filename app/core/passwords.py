import asyncio
from passlib.context import CryptContext

password_context = CryptContext(schemes=["argon2"])

async def get_password_hash(
    password: str) -> str:

    password_hash = await asyncio.to_thread(
        password_context.hash,
        password
    )
    return password_hash
    


async def is_password_correct(
    plain_password: str,
    password_hash: str) -> bool:

    is_correct = await asyncio.to_thread(
        password_context.verify,
        plain_password,
        password_hash
    )
    return is_correct
