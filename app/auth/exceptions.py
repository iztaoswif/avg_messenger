from app.core.exceptions import AppException


class AuthException(AppException):
    status_code: int = 400
    detail = "Error during auth process"


class InappropriateUsernameError(AuthException):
    status_code: int = 422
    detail = "Inappropriate username"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class InappropriatePasswordError(AuthException):
    status_code: int = 422
    detail = "Inappropriate password"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class UsernameTakenError(AuthException):
    status_code = 400
    detail = "Username is already taken"


class InvalidCredentialsError(AuthException):
    status_code = 401
    detail = "Invalid username or password"


class TokenExpiredError(AuthException):
    status_code = 401
    detail = "Token expired"


class InvalidTokenError(AuthException):
    status_code = 401
    detail = "Invalid token"


class ForbiddenError(AuthException):
    status_code = 403
    detail = "Forbidden"


class UserNotFoundError(AuthException):
    status_code = 404
    detail = "User with given id does not exist"
