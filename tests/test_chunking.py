from app.services.chunking import (
    chunk_text,
)


def test_chunking_overlap() -> None:
    text = (
        "abcdefghijklmnopqrstuvwxyz"
        * 20
    )

    chunks = chunk_text(
        text,
        chunk_size=100,
        overlap=20,
    )

    assert len(chunks) > 1
    assert chunks[0].index == 0
    assert chunks[1].index == 1
