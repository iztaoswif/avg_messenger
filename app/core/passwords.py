from passlib.context import CryptContext

password_context = CryptContext(schemes=["argon2"])

def hash_password(password: str) -> str:
    return password_context.hash(password)


def is_password_correct(plain_password: str,
password_hash: str) -> bool:
    return password_context.verify(plain_password,
    password_hash)
