from fastapi import FastAPI
from navimoderator.backend.fast_api.comments_router import router

app = FastAPI()

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}
