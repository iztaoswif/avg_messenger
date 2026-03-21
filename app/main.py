from contextlib import asynccontextmanager
from redis.asyncio import Redis
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.auth.router import auth_router
from app.core.exceptions import AppException
from app.chat.router import chat_router
from app.core.redis import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client
    yield
    await redis_client.aclose()

app = FastAPI(lifespan=lifespan)


@app.exception_handler(AppException)
async def app_auth_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)


app.mount("/", StaticFiles(directory="static"), name="static")