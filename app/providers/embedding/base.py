from abc import ABC, abstractmethod
from collections.abc import Sequence


class BaseEmbeddingProvider(ABC):
    name: str
    dimensions: int

    @abstractmethod
    def embed(
        self,
        texts: Sequence[str],
        *,
        task: str,
    ) -> list[list[float]]:
        raise NotImplementedError
