from abc import ABC, abstractmethod
from typing import Any


class BaseVectorProvider(ABC):
    @abstractmethod
    def ensure_collection(
        self,
        collection: str,
        dimensions: int,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def upsert(
        self,
        collection: str,
        points: list[dict[str, Any]],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        collection: str,
        vector: list[float],
        limit: int,
    ) -> list[dict[str, Any]]:
        raise NotImplementedError
