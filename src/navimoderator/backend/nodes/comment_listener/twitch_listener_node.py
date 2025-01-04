import os
from navimoderator.backend.core.node import Node
from navimoderator.backend.nodes.comment_listener.base_listener_node import BaseListenerNode


class TwitchListenerNode(Node, BaseListenerNode):
    def __init__(
        self, 
        input_key: list[str], 
        output_key: list[str],
    ):
        super().__init__(input_key, output_key)
        
    def _fetch_comments(self, video_id: str) -> list[str]:
        pass

    def _process_comments(self, comments):
        pass

    def execute(self, state) -> dict:
        pass