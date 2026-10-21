from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.providers.vector.base import (
    BaseVectorProvider,
)


class QdrantVectorProvider(
    BaseVectorProvider
):
    def __init__(
        self,
        url: str,
    ) -> None:
        self.client = QdrantClient(
            url=url
        )

    def ensure_collection(
        self,
        collection: str,
        dimensions: int,
    ) -> None:
        collections = (
            self.client.get_collections()
            .collections
        )

        names = {
            item.name
            for item in collections
        }

        if collection in names:
            return

        self.client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(
                size=dimensions,
                distance=Distance.COSINE,
            ),
        )

    def upsert(
        self,
        collection: str,
        points: list[dict[str, Any]],
    ) -> None:
        payload = [
            PointStruct(
                id=point["id"],
                vector=point["vector"],
                payload=point["payload"],
            )
            for point in points
        ]

        self.client.upsert(
            collection_name=collection,
            points=payload,
            wait=True,
        )

    def search(
        self,
        collection: str,
        vector: list[float],
        limit: int,
    ) -> list[dict[str, Any]]:
        response = self.client.query_points(
            collection_name=collection,
            query=vector,
            limit=limit,
            with_payload=True,
        )

        return [
            {
                "id": point.id,
                "score": float(
                    point.score
                ),
                "payload":
                    point.payload or {},
            }
            for point in response.points
        ]
