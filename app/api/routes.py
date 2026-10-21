from fastapi import (
    APIRouter,
    HTTPException,
)

from app.core.runtime import (
    embedding_provider,
    ingestion_service,
    search_service,
)
from app.schemas.models import (
    ContextRequest,
    ContextResponse,
    IngestRequest,
    SearchRequest,
    SearchResponse,
)
from app.services.context import (
    build_context,
)


router = APIRouter(
    prefix="/v1"
)


@router.get("/providers")
def providers() -> dict:
    return {
        "embedding": {
            "name":
                embedding_provider.name,
            "dimensions":
                embedding_provider.dimensions,
        },
        "vector": {
            "name": "qdrant"
        },
    }


@router.post("/ingest")
def ingest(
    payload: IngestRequest,
) -> dict:
    try:
        return (
            ingestion_service.ingest(
                payload.documents
            )
        )

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc


@router.post(
    "/search",
    response_model=SearchResponse,
)
def search(
    payload: SearchRequest,
) -> SearchResponse:
    try:
        hits = search_service.search(
            payload.query,
            payload.limit,
        )

        return SearchResponse(
            query=payload.query,
            hits=hits,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc


@router.post(
    "/context",
    response_model=ContextResponse,
)
def context(
    payload: ContextRequest,
) -> ContextResponse:
    try:
        hits = search_service.search(
            payload.query,
            payload.limit,
        )

        text, sources = (
            build_context(hits)
        )

        return ContextResponse(
            query=payload.query,
            context=text,
            sources=sources,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc
