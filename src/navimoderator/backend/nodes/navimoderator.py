from langgraph.graph import START, END, StateGraph
from langgraph.graph.graph import CompiledGraph
from typing import TypedDict, Optional

from .preprocess_node import PreprocessNode
from .process_node import ProcessNode
from .action_node import ActionNode


class NaviModeratorState(TypedDict):
    streamer_login: str
    access_token: str
    refresh_token: str
    user_id: str
    comments: list[dict]
    preprocessed_comments: Optional[list[dict]]
    processed_comments: Optional[list[dict]]


class NaviModerator:
    def __init__(
        self, 
    ):
        pass

    def _preprocess_node(self, state: NaviModeratorState) -> dict:
        comments = state["comments"]
        preprocessed_comments = PreprocessNode().execute(comments)
        return {"preprocessed_comments": preprocessed_comments}

    def _process_node(self, state: NaviModeratorState) -> dict:
        preprocessed_comments = state["preprocessed_comments"]
        processed_comments = ProcessNode().execute(preprocessed_comments)
        return {"processed_comments": processed_comments}

    def _action_node(self, state: NaviModeratorState) -> dict:
        processed_comments = state["processed_comments"]
        processed_comments = ActionNode().execute(processed_comments)
        return {"processed_comment": processed_comments}

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

    comments = [
        {
        "timestamp": "2025-03-14T12:34:56Z", 
        "user_name": "@someone_in_chat", 
        "comment_id": "xxxx", 
        "comment": "Hello!", 
        }, 
        {
        "timestamp": "2025-03-14T12:34:56Z", 
        "user_name": "@someone_in_chat", 
        "comment_id": "xxxx", 
        "comment": "これは誹謗中傷コメントです", 
        }, 
    ]
    input_data = {
        "streamer_login": "test", 
        "access_token": "test", 
        "refresh_token": "test", 
        "user_id": "test", 
        "comments": comments, 
        "preprocessed_comments": [], 
        "processed_comments": [], 
    }

    nave_moderator = NaviModerator().build_graph()
    result = nave_moderator.invoke(input_data)