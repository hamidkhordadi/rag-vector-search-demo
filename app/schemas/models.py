from typing import Any

from pydantic import BaseModel, Field


class DocumentInput(BaseModel):
    document_id: str = Field(
        min_length=1
    )
    title: str = Field(
        min_length=1
    )
    text: str = Field(
        min_length=1
    )
    source: str = Field(
        min_length=1
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class IngestRequest(BaseModel):
    documents: list[DocumentInput]


class SearchRequest(BaseModel):
    query: str = Field(
        min_length=1
    )
    limit: int = Field(
        default=5,
        ge=1,
        le=20,
    )


class SearchHit(BaseModel):
    score: float
    document_id: str
    chunk_id: str
    title: str
    text: str
    source: str
    metadata: dict[str, Any]


class SearchResponse(BaseModel):
    query: str
    hits: list[SearchHit]


class ContextRequest(BaseModel):
    query: str = Field(
        min_length=1
    )
    limit: int = Field(
        default=4,
        ge=1,
        le=10,
    )


class ContextResponse(BaseModel):
    query: str
    context: str
    sources: list[dict[str, Any]]
