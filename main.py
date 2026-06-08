from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import api_router
from config.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: add a logger(you can use loguru)
    # TODO: add a db
    # TODO: refactor frontend


    print("Starting Stamford StudyAssist API")

    # init_db()

    yield

    print("Stopping Stamford StudyAssist API")


app = FastAPI(
    title="Stamford StudyAssist API",
    description=(
        "AI-powered learning assistant for Stamford International University. "
        "Supports lecture slide uploads, AI chat, quiz generation, "
        "lecture summarization, and RAG-based retrieval."
    ),
    version="2.0.0",
    lifespan=lifespan,
)


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:8501",
#         "http://127.0.0.1:8501",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get(
    "/",
    summary="API Information",
    description="Returns basic information about the StudyAssist backend."
)
def root():
    return {
        "application": "Stamford StudyAssist API",
        "version": "2.0.0",
        "status": "running",
        "provider": settings.ai_provider
    }

@app.get(
    "/health",
    summary="Health Check",
    description="Checks whether the API is currently operational."
)
def health():
    return {
        "status": "healthy"
    }


app.include_router(api_router)