from spoilbuster.backend.core.node import Node
from spoilbuster.backend.nodes.youtube_listener_node import YoutubeListenerNode
from spoilbuster.backend.nodes.game_data_node import GameDataNode
from spoilbuster.backend.nodes.structured_llm_node import StructuredLLMNode

NODE_MAPPING = {
    "youtube_listener_node": YoutubeListenerNode,
    "game_data_node": GameDataNode,
    "structured_llm_node": StructuredLLMNode,
}
class NodeFactory:
    @staticmethod
    def create_node(node_name: str, **kwargs) -> Node:
        """
        Factory method for dynamically generating nodes
        :param node_name: Node name
        :param kwargs: Additional arguments when creating a node
        :return: Node instance
        """
        if node_name not in NODE_MAPPING:
            raise ValueError(f"Unknown node type: {node_name}")   
        return NODE_MAPPING[node_name](**kwargs)