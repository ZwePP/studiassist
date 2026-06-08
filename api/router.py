from fastapi import APIRouter

from api.routes.upload_routes import router as upload_router
from api.routes.question_routes import router as ask_router
from api.routes.quiz_routes import router as quiz_router
from api.routes.summarize_routes import router as summary_router

api_router = APIRouter(
    prefix="/api",
)


api_router.include_router(
    upload_router,
    tags=["Document Upload"],
)

api_router.include_router(
    ask_router,
    tags=["AI Study Chat"],
)

api_router.include_router(
    quiz_router,
    tags=["Quiz Generation"],
)

api_router.include_router(
    summary_router,
    tags=["Lecture Summary"],
)