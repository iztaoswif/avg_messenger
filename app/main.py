from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.auth.router import auth_router
from app.auth.exceptions import AuthException
from app.chat.exceptions import ChatException
from app.chat.router import chat_router
from app.db.models import metadata
from app.db.engine import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    yield

app = FastAPI(lifespan=lifespan)


@app.exception_handler(AuthException)
async def app_auth_exception_handler(request: Request, exc: AuthException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(ChatException)
async def app_chat_exception_handler(request: Request, exc: ChatException):
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