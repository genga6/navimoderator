from langgraph.graph import START, END, StateGraph
from langgraph.graph.graph import CompiledGraph
from typing import TypedDict

from preprocess_node import PreprocessNode
from process_node import ProcessNode
from action_node import ActionNode


class NaviModeratorState(TypedDict):
    comments: list
    preprocessed_comments: list
    processed_comments: list
    action: str


class NaviModerator:
    def __init__(
        self, 
    ):
        pass

    def _preprocess_node(self, state: NaviModeratorState) -> dict:
        comments = state["comments"]
        preprocessed_comments = PreprocessNode(

        ).execute(comments)
        return {"preprocessed_comments": preprocessed_comments}

    def _process_node(self, state: NaviModeratorState) -> dict:
        preprocessed_comments = state["preprocessed_comments"]
        processed_comments = ProcessNode(

        ).execute(preprocessed_comments)
        return {"processed_comments": processed_comments}

    def _action_node(self, state: NaviModeratorState) -> dict:
        processed_comments = state["processed_comments"]
        action = ActionNode(

        ).execute(processed_comments)
        return {"action": action}

    def build_graph(self) -> CompiledGraph:
        graph_builder = StateGraph(NaviModeratorState)
        # make nodes
        graph_builder.add_node("preprocess_node", self._preprocess_node)
        graph_builder.add_node("process_node", self._process_node)
        graph_builder.add_node("action_node", self._action_node)
        # make edges
        graph_builder.add_edge(START, "preprocess_node")
        graph_builder.add_edge("preprocess_node", "process_node")
        graph_builder.add_edge("process_node", "action_node")        
        graph_builder.add_edge("action_node", END)

        return graph_builder.compile()


if __name__ == "__main__":

    comments = ["これは", "テスト", "データです。"]
    input_data = {
        "comments": comments
    }

    nave_moderator = NaviModerator().build_graph()
    result = nave_moderator.invoke(input_data)