from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from users import router as users_router
from posts import router as posts_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "FastAPI is running"}

app.include_router(users_router)
app.include_router(posts_router)
