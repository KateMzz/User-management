from fastapi import HTTPException

from utils.logconf import logger


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Resource not found")


class BlacklistedToken(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Token is blacklisted")


class UserCreateError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User create error, check your data")


class UserExists(HTTPException):
    def __init__(self, error_info):
        super().__init__(status_code=400, detail=error_info)


class ExceptionHandler:
    def handle_unique_constraint_error(self, e):
        error_info = e.orig.args[0]
        if "DETAIL" in error_info:
            error_info = error_info.split("DETAIL:  ")[1]
            raise UserExists(error_info)
        logger.error(e)
