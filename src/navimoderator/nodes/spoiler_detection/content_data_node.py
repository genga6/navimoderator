import requests
from navimoderator.backend.core.node import Node

class ContentDataNode(Node):
    def __init__(
        self, 
        input_key: list[str], 
        output_key: list[str],
    ):
        super().__init__(input_key, output_key)

    def _fetch_content_data(self, content_title: str) -> dict:
        pass    #TODO: PerplexityAPIから情報取得する

    def execute(self, state) -> dict:
        content_title = state[self.input_key[0]]

        content_data = self._fetch_content_data(content_title)
        if not content_data:
            raise ValueError(f"Content info not found for {content_title}")
        
        return {   
            self.output_key[0]: content_data,
        }