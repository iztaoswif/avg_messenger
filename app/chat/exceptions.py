from app.core.exceptions import AppException


class ChatException(AppException):
    status_code: int = 400
    detail = "Unknown error occured"


class InappropriateMessageTextError(ChatException):
    status_code: int = 422
    detail = "Inappropriate content"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class InappropriateChatNameError(ChatException):
    status_code: int = 422
    detail = "Inappropriate chat name"


class InappropriateChatIdError(ChatException):
    status_code: int = 422
    detail = "Inappropriate chat id"


class AlreadyChatMemberError(ChatException):
    status_code: int = 409
    detail = "The user is already a member of the given chat"


class ChatNotFoundError(ChatException):
    status_code: int = 404
    detail = "Chat not found"


class SelfReferencingError(ChatException):
    status_code: int = 422
    detail = "You can not choose yourself"
