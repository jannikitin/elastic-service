from api.endpoints.login_endpoints import login_router
from api.endpoints.user_endpoints import user_router
from fastapi import FastAPI

app = FastAPI(title="Elastic")

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(login_router, prefix="/login", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "OK!"}
