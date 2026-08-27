from uuid import UUID
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from core.helper_types import UserId
from core.token import decode_access_token
from auth.exceptions import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> UserId:
    payload = decode_access_token(token)
    user_id = payload.get("sub")

    if user_id is None:
        raise InvalidTokenError()

    return UUID(user_id)
