import os
from IPython.display import Image
from langgraph.graph.graph import CompiledGraph

from navimoderator.backend.nodes.navimoderator import NaviModerator

IMAGE_SAVE_DIR = "/workspaces/navimoderator/images"


def save_mermaid(
    graph: CompiledGraph, 
    file_name: str, 
    save_dir: str = IMAGE_SAVE_DIR
):
    mermaid_text = graph.get_graph().draw_mermaid()
    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, file_name), "w") as f:
        f.write(mermaid_text)
    print(f"Mermaid記法を保存しました: {os.path.join(save_dir, file_name)}")


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

    navi_moderator = NaviModerator().build_graph()
    result = navi_moderator.invoke(input_data)

    save_mermaid(graph=navi_moderator, file_name="navimoderator.mmd")

