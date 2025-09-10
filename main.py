from fastapi import FastAPI
from api.user import router as user_router
from api.investments import router as investments_router


app = FastAPI(
    title="Mutual Fund Broker Application",
    description="Mutual Fund Broker Application",
    version="1.0.0"
)

# Include routers
app.include_router(user_router, prefix="")
app.include_router(investments_router, prefix="")


@app.get("/")
async def read_root():
    return {"message": "Welcome to Mutual Fund Broker Application!", "status": "running"}

