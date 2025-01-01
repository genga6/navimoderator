from spoilbuster.backend.core.node import Node

NODE_MAPPING = {}

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