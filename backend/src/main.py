import os
from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import redis.asyncio

from auth.router import auth_router
from chat.router import chat_router
from core.exceptions import AppException

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_url = os.environ["REDIS_URL"]
    redis_client = redis.asyncio.from_url(
        redis_url,
        decode_responses=True,
        max_connections=30
    )
    
    app.state.redis = redis_client
    yield
    await app.state.redis.aclose()


if os.environ["APP_ENV"] == "prod":
    app = FastAPI(
        lifespan=lifespan,
        docs_url=None, 
        redoc_url=None,
        openapi_url=None
    )
else:
    app = FastAPI(
        lifespan=lifespan
    )


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


ALLOWED_ORIGINS = os.environ["ALLOWED_ORIGINS"].split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router)
api_router.include_router(chat_router)
app.include_router(api_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")
