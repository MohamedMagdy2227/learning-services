from fastapi import FastAPI
from src.routers import base
from src.routers.quiz_routers import gen_router, quiz_router
from src.ai_engine.quiz_feature.BankQuestions_engine.openai_client_dependency import (
    init_openai_client as init_quiz_openai,
    close_openai_client as close_quiz_openai,
)

from src.ai_engine.summarization_engine.openai_client_dependency import (
    init_openai_client as init_summary_openai,
    close_openai_client as close_summary_openai,
)

from .routers import roadmap, mindmap, summarization_router

from src.ai_engine.data_fetchers.qdrant_client_dependency import (
    init_qdrant_client,
    close_qdrant_client,
)
from src.ai_engine.quiz_feature.quiz_qdrant_client import ensure_quiz_collection_exists

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_quiz_openai()
    await init_summary_openai()

    try:
        await init_qdrant_client()
        await ensure_quiz_collection_exists()

    except Exception:
        await close_quiz_openai()
        await close_summary_openai()
        await close_qdrant_client()
        raise


@app.on_event("shutdown")
async def shutdown_event():
    try:
        await close_quiz_openai()
        await close_summary_openai()
    finally:
        await close_qdrant_client()


app.include_router(base.base_router)


app.include_router(gen_router)
app.include_router(quiz_router)

app.include_router(summarization_router.summ_router)
app.include_router(roadmap.roadmap_router)
app.include_router(mindmap.mindmap_router)
