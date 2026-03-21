class AppException(Exception):
    status_code: int = 400
    detail = "Unknown error occured"


class RateLimitedError(AppException):
    status_code: int = 429
    detail = "Too many requests per unit of time"
