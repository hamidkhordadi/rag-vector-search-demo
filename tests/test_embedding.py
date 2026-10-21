from app.providers.embedding.local_hash import (
    LocalHashEmbeddingProvider,
)


def test_embedding_is_deterministic() -> None:
    provider = (
        LocalHashEmbeddingProvider(
            dimensions=64
        )
    )

    first = provider.embed(
        ["hello world"],
        task="search_document",
    )[0]

    second = provider.embed(
        ["hello world"],
        task="search_document",
    )[0]

    assert first == second
    assert len(first) == 64


def test_same_words_are_similar() -> None:
    provider = (
        LocalHashEmbeddingProvider(
            dimensions=128
        )
    )

    vectors = provider.embed(
        [
            "shipping tracking delivery",
            "delivery shipping tracking",
            "banana orange fruit",
        ],
        task="search_document",
    )

    def dot(a, b):
        return sum(
            x * y
            for x, y in zip(
                a,
                b,
                strict=True,
            )
        )

    assert (
        dot(
            vectors[0],
            vectors[1],
        )
        >
        dot(
            vectors[0],
            vectors[2],
        )
    )
