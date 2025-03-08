from langgraph.graph import START, END, StateGraph
from typing import TypedDict
from langgraph.graph.graph import CompiledGraph
from preprocess_node import PreprocessNode
from process_node import ProcessNode


class NaviModeratorState(TypedDict):
    streamer_login: str
    access_token: str
    refresh_token: str
    comment: str
    user_id: str
    action: str # "pass" or "delete" or "timeout"


class NaviModerator:
    def __init__(self):
        pass
    
    def build_graph(self) -> CompiledGraph:
        preprocess_node = PreprocessNode(
            
        ).build_graph()

        process_node = ProcessNode(
            #llm_name="gpt-4o-2024-11-20",
        ).build_graph()

        graph_builder = StateGraph(NaviModeratorState)
        # make nodes
        graph_builder.add_node("preprocess_node", preprocess_node)
        graph_builder.add_node("process_node", process_node)
        # make edges
        graph_builder.add_edge(START, "preprocess_node")
        graph_builder.add_edge("preprocess_node", "process_node")
        graph_builder.add_edge("process_node", END)

        return graph_builder.compile()


if __name__ == "__main__":
    pass