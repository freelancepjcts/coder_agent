# app/exceptions/handlers.py

from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import traceback

async def exception_handler(request: Request, exc: Exception):
    status_code = 500
    message = "Internal Server Error"
    extra = {}

    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        message = exc.detail

    elif isinstance(exc, RequestValidationError):
        status_code = 422
        message = "Validation Error"
        extra["errors"] = exc.errors()

    response = {
        "success": False,
        "message": message,
        **extra
    }

    response["trace"] = traceback.format_exc()
    return JSONResponse(status_code=status_code, content=response)