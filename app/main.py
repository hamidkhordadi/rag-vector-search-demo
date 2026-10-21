from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="RAG Vector Search Demo",
    version="1.0.0",
    description=(
        "Production-inspired RAG retrieval "
        "pipeline with FastAPI and Qdrant."
    ),
)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service":
            "RAG Vector Search Demo",
    }


app.include_router(router)
