import uvicorn
from api.endpoints.admin_endpoints import admin_router
from api.endpoints.login_endpoints import login_router
from api.endpoints.user_endpoints import user_router
from fastapi import FastAPI

app = FastAPI(title="Elastic")

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(login_router, prefix="/login", tags=["auth"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])


@app.get("/")
async def root():
    return {"message": "OK!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
