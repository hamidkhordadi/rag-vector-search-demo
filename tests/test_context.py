from app.schemas.models import SearchHit
from app.services.context import (
    build_context,
)


def test_context_has_sources() -> None:
    hit = SearchHit(
        score=0.9,
        document_id="doc-1",
        chunk_id="doc-1:0",
        title="Demo",
        text="Example passage",
        source="synthetic://demo",
        metadata={},
    )

    context, sources = (
        build_context([hit])
    )

    assert "[Source 1]" in context
    assert (
        sources[0]["source"]
        == "synthetic://demo"
    )
