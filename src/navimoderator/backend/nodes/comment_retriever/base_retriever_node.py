from abc import ABC, abstractmethod
from typing import AsyncIterator

class BaseRetrieverNode(ABC):
    @abstractmethod
    def _fetch_comments(self, streamer_id: str) -> AsyncIterator[dict]:
        pass