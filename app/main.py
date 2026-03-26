import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.redis import create_redis_client
from app.auth.router import auth_router
from app.chat.router import chat_router
from app.core.exceptions import AppException

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = create_redis_client()
    yield
    await app.state.redis.aclose()

app = FastAPI(
    lifespan=lifespan,
    docs_url=None, 
    redoc_url=None,
    openapi_url=None
)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.get("/docs", include_in_schema=False)
async def get_documentation(request: Request):
    client_host = request.client.host
    if client_host not in ("127.0.0.1", "localhost"):
        raise HTTPException(status_code=404)
    
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(request: Request):
    client_host = request.client.host
    if client_host not in ("127.0.0.1", "localhost"):
        raise HTTPException(status_code=404)
    from fastapi.openapi.utils import get_openapi
    return get_openapi(title="Average Messenger API", version="1.0.0", routes=app.routes)

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")