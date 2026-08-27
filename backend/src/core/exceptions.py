class AppException(Exception):
    status_code: int = 400
    detail = "Unknown error occured"


class ForbiddenError(AppException):
    status_code: int = 403
    detail = "Access denied"


class NotAMemberError(ForbiddenError):
    detail = "Not a member of the chat"
