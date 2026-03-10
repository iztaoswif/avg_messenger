from fastapi import Depends
from app.core.token import decode_access_token
from app.auth.oauth import oauth2_scheme
from app.auth.exceptions import InvalidTokenError

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    payload = decode_access_token(token)
    user_id = payload.get("sub")

    if user_id is None:
        raise InvalidTokenError()

    return int(user_id)
