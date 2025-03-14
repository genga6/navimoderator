from langgraph.graph import START, END, StateGraph
from langgraph.graph.graph import CompiledGraph
from typing import TypedDict, Optional

from navimoderator.backend.nodes.preprocess_node import PreprocessNode
from navimoderator.backend.nodes.process_node import ProcessNode
from navimoderator.backend.nodes.action_node import ActionNode



class NaviComment(TypedDict, total=False):
    timestamp: str
    user_name: str
    comment_id: str
    comment: str
    translated_comment: str
    is_harassment: bool
    moderator_action: str   # "pass" or "post" or "delete"

class NaviModeratorState(TypedDict):
    streamer_login: str
    access_token: str
    refresh_token: str
    comments: list[NaviComment]


class NaviModerator:
    def __init__(
        self,
        llm_name: str, 
        compute_env: str, 
        is_translation: bool, 
        is_moderation: bool,  
    ):
        self.llm_name = llm_name
        self.compute_env = compute_env
        self.is_translation = is_translation
        self.is_moderation = is_moderation

    def _preprocess_node(self, state: NaviModeratorState) -> dict:
        comments = state["comments"]
        updated_comments = PreprocessNode().execute(comments)
        return {"comments": updated_comments}

    def _process_node(self, state: NaviModeratorState) -> dict:
        comments = state["comments"]
        updated_comments = ProcessNode().execute(comments)
        return {"comments": updated_comments}

    def _action_node(self, state: NaviModeratorState) -> dict:
        comments = state["comments"]
        updated_comments = ActionNode().execute(comments)
        return {"comments": updated_comments}
    
    def _has_processed_comments(self, state: NaviModeratorState) -> str:
        comments = state["comments"]
        if all("is_harassment" in c for c in comments):     #NOTE: `is_harassment`以外のフラグを検討する
            return "skip_processing" 
        return "do_processing"
                
    def build_graph(self) -> CompiledGraph:
        graph_builder = StateGraph(NaviModeratorState)
        # make nodes
        graph_builder.add_node("preprocess_node", self._preprocess_node)
        graph_builder.add_node("process_node", self._process_node)
        graph_builder.add_node("action_node", self._action_node)
        # make edges
        graph_builder.add_conditional_edges(
            START, 
            path=self._has_processed_comments, 
            path_map={
                "do_processing": "preprocess_node", 
                "skip_processing": "action_node"
            }
        )
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
        "comments": comments, 
    }

    llm_name = "llm_name"
    compute_env = "browser"
    is_translation = True
    is_moderation = True

    navi_moderator = NaviModerator(
        llm_name=llm_name, 
        compute_env=compute_env, 
        is_translation=is_translation, 
        is_moderation=is_moderation, 
    ).build_graph()
    result = navi_moderator.invoke(input_data)
    print(result)