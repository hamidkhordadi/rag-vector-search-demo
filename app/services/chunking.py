from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    index: int
    text: str


def chunk_text(
    text: str,
    *,
    chunk_size: int,
    overlap: int,
) -> list[TextChunk]:
    normalized = " ".join(
        text.split()
    )

    if not normalized:
        return []

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    chunks: list[TextChunk] = []

    start = 0
    index = 0

    while start < len(normalized):
        end = min(
            start + chunk_size,
            len(normalized),
        )

        piece = normalized[
            start:end
        ].strip()

        if piece:
            chunks.append(
                TextChunk(
                    index=index,
                    text=piece,
                )
            )

            index += 1

        if end >= len(normalized):
            break

        start = end - overlap

    return chunks
