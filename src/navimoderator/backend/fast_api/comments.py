import httpx
from fastapi import APIRouter, HTTPException
from ..nodes.navimoderator import NaviModerator

router = APIRouter()
navi_moderator = NaviModerator().build_graph()

@router.post("/moderate")
async def moderate_comments(payload: dict):
    """
    Twitch APIからコメントや推論結果を受け取って、
    LangGraphワークフローを実行する。

    payload = {
        "streamer_login": streamer_login, 
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "comments": [  # コメントはリストとして扱う
            {
                "timestamp": "2025-03-14T12:34:56Z",
                "user_name": "someone_in_chat",
                "comment_id": "abcd1234",
                "comment": "Hello!"
            },
            {
                "timestamp": "2025-03-14T12:34:56Z",
                "user_name": "someone_in_chat",
                "comment_id": "abcd1234",
                "comment": "Hello!"
            }
        ],
        "preprocessed_comments": [],  # LangGraph のノードで更新
        "processed_comments": [],  # LangGraph の最終出力
    }
    """
    result = navi_moderator.invoke(payload)
    processed_comments = result["processed_comments"]

    return {
        "processed_comments": processed_comments
    }


