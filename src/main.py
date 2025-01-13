from api.endpoints.user_endpoints import user_router
from fastapi import FastAPI

app = FastAPI(title="Elastic")

app.include_router(user_router, prefix="/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "OK!"}
