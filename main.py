from fastapi import FastAPI

from db.base import database
from endpoints import users, pairs
import uvicorn

app = FastAPI(title="Demo Api")
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(pairs.router, prefix="/pairs", tags=["pairs"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
