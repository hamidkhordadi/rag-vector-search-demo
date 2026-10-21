from app.schemas.models import SearchHit


def build_context(
    hits: list[SearchHit],
) -> tuple[
    str,
    list[dict],
]:
    blocks = []
    sources = []

    for index, hit in enumerate(
        hits,
        start=1,
    ):
        blocks.append(
            f"[Source {index}] "
            f"{hit.title}\n"
            f"{hit.text}"
        )

        sources.append(
            {
                "source_number":
                    index,
                "document_id":
                    hit.document_id,
                "chunk_id":
                    hit.chunk_id,
                "title":
                    hit.title,
                "source":
                    hit.source,
                "score":
                    hit.score,
            }
        )

    return (
        "\n\n".join(blocks),
        sources,
    )
