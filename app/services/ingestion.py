from hashlib import sha256
from uuid import UUID

from app.providers.embedding.base import (
    BaseEmbeddingProvider,
)
from app.providers.vector.base import (
    BaseVectorProvider,
)
from app.schemas.models import DocumentInput
from app.services.chunking import (
    chunk_text,
)


def stable_point_id(
    document_id: str,
    chunk_index: int,
) -> str:
    digest = sha256(
        (
            f"{document_id}:"
            f"{chunk_index}"
        ).encode("utf-8")
    ).digest()

    raw = bytearray(
        digest[:16]
    )

    raw[6] = (
        raw[6] & 0x0F
    ) | 0x40

    raw[8] = (
        raw[8] & 0x3F
    ) | 0x80

    return str(
        UUID(bytes=bytes(raw))
    )


class IngestionService:
    def __init__(
        self,
        *,
        embedding:
            BaseEmbeddingProvider,
        vector:
            BaseVectorProvider,
        collection: str,
        chunk_size: int,
        chunk_overlap: int,
    ) -> None:
        self.embedding = embedding
        self.vector = vector
        self.collection = collection
        self.chunk_size = chunk_size
        self.chunk_overlap = (
            chunk_overlap
        )

    def ingest(
        self,
        documents:
            list[DocumentInput],
    ) -> dict:
        self.vector.ensure_collection(
            self.collection,
            self.embedding.dimensions,
        )

        points = []
        chunk_count = 0

        for document in documents:
            chunks = chunk_text(
                document.text,
                chunk_size=(
                    self.chunk_size
                ),
                overlap=(
                    self.chunk_overlap
                ),
            )

            texts = [
                chunk.text
                for chunk in chunks
            ]

            vectors = (
                self.embedding.embed(
                    texts,
                    task="search_document",
                )
            )

            for chunk, vector in zip(
                chunks,
                vectors,
                strict=True,
            ):
                chunk_id = (
                    f"{document.document_id}"
                    f":{chunk.index}"
                )

                points.append(
                    {
                        "id":
                            stable_point_id(
                                document.document_id,
                                chunk.index,
                            ),
                        "vector":
                            vector,
                        "payload": {
                            "document_id":
                                document.document_id,
                            "chunk_id":
                                chunk_id,
                            "chunk_index":
                                chunk.index,
                            "title":
                                document.title,
                            "text":
                                chunk.text,
                            "source":
                                document.source,
                            "metadata":
                                document.metadata,
                        },
                    }
                )

                chunk_count += 1

        if points:
            self.vector.upsert(
                self.collection,
                points,
            )

        return {
            "documents":
                len(documents),
            "chunks":
                chunk_count,
            "embedding_provider":
                self.embedding.name,
            "dimensions":
                self.embedding.dimensions,
        }
