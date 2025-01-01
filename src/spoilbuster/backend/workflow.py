from typing import TypedDict
from langgraph.graph import StateGraph
from spoilbuster.backend.core.factory import NodeFactory


class State(TypedDict):
    video_id: str
    game_title: str
    game_info: dict
    user_progress: str
    youtube_comments: list[str]
    game_flagged_comments: list[str]
    vague_flagged_comments: list[str]
    normalized_progress: str
    refined_comments: list[str]

class SpoilBusterWorkflow:
    def __init__(
        self, 
        video_id: str,
        comments: list[str],
    ):
        self.video_id = video_id
        self.comments = comments
    
        self.graph_builder = StateGraph(State)
        self.graph_builder.add_node(
            "youtube_listener_node",
            NodeFactory.create_node(
                node_name="youtube_listener_node",
                input_key=["video_id"],
                output_key=["youtube_comments"],
            ), 
        )
        self.graph_builder.add_node(
            "game_data_node",
            NodeFactory.create_node(
                node_name="game_data_node",
                input_key=["game_title"],
                output_key=["game_flagged_comments", "game_info"],
            ), 
        )
        self.graph_builder.add_node(
            "vague_check_node",
            NodeFactory.create_node(
                node_name="structured_llm_node",
                input_key=["game_flagged_comments"],
                output_key=["vague_flagged_comments"],
            ), 
        )
        self.graph_builder.add_node(
            "llm_refiner_node",
            NodeFactory.create_node(
                node_name="structured_llm_node",
                input_key=["vague_flagged_comments", "game_info", "normalized_progress"],
                output_key=["refined_comments"],
                llm_name="gpt-3.5-turbo",
                prompt_template="What is the game about?",
            ), 
        )
        self.graph_builder.add_edge(["youtube_listener_node", "user_progress_node"], "game_data_node")
        self.graph_builder.add_edge("game_data_node", "vague_check_node")
        self.graph_builder.add_edge("vague_check_node", "llm_refiner_node")
        self.graph_builder.set_entry_point("youtube_listener_node")
        self.graph_builder.set_finish_point("llm_refiner_node")
        self.graph = self.graph_builder.compile()

    def __call__(self, state: State) -> dict:
        result = self.graph.invoke(state, debug=True)
        return result