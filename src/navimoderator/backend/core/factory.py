from navimoderator.backend.core.node import Node
from navimoderator.backend.nodes.comment_retriever.youtube_retriever_node import YoutubeRetrieverNode
from navimoderator.backend.nodes.spoiler_detection.content_data_node import ContentDataNode
from navimoderator.backend.nodes.structured_llm_node import StructuredLLMNode

NODE_MAPPING = {
    "youtube_retriever_node": YoutubeRetrieverNode,
    "content_data_node": ContentDataNode,
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