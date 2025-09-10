from fastapi import FastAPI
from api.user import router as user_router
from api.investments import router as investments_router
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from api.utils import format_error_response


app = FastAPI(
    title="Mutual Fund Broker Application",
    description="Mutual Fund Broker Application",
    version="1.0.0"
)

# Include routers
app.include_router(user_router, prefix="")
app.include_router(investments_router, prefix="")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return format_error_response(exc.status_code, exc.detail)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # messages = [f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()]
    messages = [{err['loc'][-1]: err['msg']} for err in exc.errors()]
    return format_error_response(422, messages)

