import traceback

from fastapi import HTTPException

from app.logger import get_logger

log = get_logger(__name__)


class ErrorHandler:
    def handle_error(self, error: Exception) -> None:
        if isinstance(error, HTTPException):
            status_code = error.status_code
            error_message = error.detail
            if isinstance(error_message, bytes):
                error_message = error_message.decode("utf-8")
        elif "not found" in str(error):
            status_code = 400
            error_message = str(error)
        else:
            status_code = 500
            error_message = "Internal Server Error"

        log.error(error_message)
        traceback.print_exc()
        raise HTTPException(status_code=status_code, detail=error_message)


error_handler = ErrorHandler()
