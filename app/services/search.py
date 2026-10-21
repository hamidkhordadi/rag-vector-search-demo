from app.providers.embedding.base import (
    BaseEmbeddingProvider,
)
from app.providers.vector.base import (
    BaseVectorProvider,
)
from app.schemas.models import SearchHit


class SearchService:
    def __init__(
        self,
        *,
        embedding:
            BaseEmbeddingProvider,
        vector:
            BaseVectorProvider,
        collection: str,
    ) -> None:
        self.embedding = embedding
        self.vector = vector
        self.collection = collection

    def search(
        self,
        query: str,
        limit: int,
    ) -> list[SearchHit]:
        vector = self.embedding.embed(
            [query],
            task="search_query",
        )[0]

        rows = self.vector.search(
            self.collection,
            vector,
            limit,
        )

        hits = []

        for row in rows:
            payload = row["payload"]

            hits.append(
                SearchHit(
                    score=row["score"],
                    document_id=str(
                        payload.get(
                            "document_id",
                            "",
                        )
                    ),
                    chunk_id=str(
                        payload.get(
                            "chunk_id",
                            "",
                        )
                    ),
                    title=str(
                        payload.get(
                            "title",
                            "",
                        )
                    ),
                    text=str(
                        payload.get(
                            "text",
                            "",
                        )
                    ),
                    source=str(
                        payload.get(
                            "source",
                            "",
                        )
                    ),
                    metadata=dict(
                        payload.get(
                            "metadata",
                            {},
                        )
                    ),
                )
            )

        return hits
