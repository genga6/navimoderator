from abc import ABC, abstractmethod

class BaseListenerNode(ABC):
    @abstractmethod
    def _fetch_comments(self, video_id: str) -> list[str]:
        pass

    @abstractmethod
    def _process_comments(self, comments) -> list[str]:
        pass
