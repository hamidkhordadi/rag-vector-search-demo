from collections.abc import Sequence
from hashlib import sha256
from math import sqrt
import re

from app.providers.embedding.base import (
    BaseEmbeddingProvider,
)


class LocalHashEmbeddingProvider(
    BaseEmbeddingProvider
):
    name = "local-hash"

    def __init__(
        self,
        dimensions: int = 256,
    ) -> None:
        if dimensions < 32:
            raise ValueError(
                "dimensions must be >= 32"
            )

        self.dimensions = dimensions

    @staticmethod
    def _tokens(
        text: str,
    ) -> list[str]:
        return re.findall(
            r"[\w'-]+",
            text.lower(),
            flags=re.UNICODE,
        )

    def _embed_one(
        self,
        text: str,
    ) -> list[float]:
        vector = [
            0.0
            for _ in range(
                self.dimensions
            )
        ]

        for token in self._tokens(text):
            digest = sha256(
                token.encode("utf-8")
            ).digest()

            index = int.from_bytes(
                digest[:4],
                "big",
            ) % self.dimensions

            sign = (
                1.0
                if digest[4] % 2 == 0
                else -1.0
            )

            vector[index] += sign

        norm = sqrt(
            sum(
                value * value
                for value in vector
            )
        )

        if norm > 0:
            vector = [
                value / norm
                for value in vector
            ]

        return vector

    def embed(
        self,
        texts: Sequence[str],
        *,
        task: str,
    ) -> list[list[float]]:
        if task not in {
            "search_document",
            "search_query",
        }:
            raise ValueError(
                "unsupported embedding task"
            )

        return [
            self._embed_one(text)
            for text in texts
        ]
