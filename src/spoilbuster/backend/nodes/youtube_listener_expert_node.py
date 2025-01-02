import os
from spoilbuster.backend.core.node import Node
from googleapiclient.discovery import build

class YoutubeListenerExpertNode(Node):
    def __init__(
        self, 
        input_key: list[str], 
        output_key: list[str],
    ):
        super().__init__(input_key, output_key)

    def _extract_features(self, comment: str) -> dict:
        return [{"text": c, "is_vague": self.check_vagueness(c)} for c in comments] #TODO: LLM使用

    def execute(self, state) -> dict:
        comment = state[self.input_key[0]]
        
        return {   
            self.output_key[0]: self._extract_features(comment),
        }
