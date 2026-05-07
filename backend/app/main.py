import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes import router
from backend.app.core.config import settings
from backend.app.core.session_store import cleanup_expired_sessions


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start session cleanup background task on server boot
    task = asyncio.create_task(cleanup_expired_sessions())
    yield
    # Cancel the cleanup task cleanly on server shutdown
    task.cancel()


app = FastAPI(
    title="Islamic RAG API",
    description="API for answering Islamic questions using retrieval-augmented generation.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Islamic RAG API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
