from app.core.settings import settings
from app.providers.embedding.local_hash import (
    LocalHashEmbeddingProvider,
)
from app.providers.vector.qdrant import (
    QdrantVectorProvider,
)
from app.services.ingestion import (
    IngestionService,
)
from app.services.search import (
    SearchService,
)


embedding_provider = (
    LocalHashEmbeddingProvider(
        dimensions=(
            settings.embedding_dimensions
        )
    )
)

vector_provider = (
    QdrantVectorProvider(
        url=settings.qdrant_url
    )
)

ingestion_service = (
    IngestionService(
        embedding=embedding_provider,
        vector=vector_provider,
        collection=(
            settings.qdrant_collection
        ),
        chunk_size=(
            settings.chunk_size
        ),
        chunk_overlap=(
            settings.chunk_overlap
        ),
    )
)

search_service = SearchService(
    embedding=embedding_provider,
    vector=vector_provider,
    collection=(
        settings.qdrant_collection
    ),
)
