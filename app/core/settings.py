from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv(
        "APP_NAME",
        "RAG Vector Search Demo",
    )

    qdrant_url: str = os.getenv(
        "QDRANT_URL",
        "http://qdrant:6333",
    )

    qdrant_collection: str = os.getenv(
        "QDRANT_COLLECTION",
        "demo_documents",
    )

    embedding_dimensions: int = int(
        os.getenv(
            "EMBEDDING_DIMENSIONS",
            "256",
        )
    )

    chunk_size: int = int(
        os.getenv(
            "CHUNK_SIZE",
            "420",
        )
    )

    chunk_overlap: int = int(
        os.getenv(
            "CHUNK_OVERLAP",
            "80",
        )
    )


settings = Settings()
