from contextlib import asynccontextmanager
from app.core.redis import create_redis_client
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.auth.router import auth_router
from app.core.exceptions import AppException
from app.chat.router import chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = create_redis_client()
    yield
    await app.state.redis.aclose()

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