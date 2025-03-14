import httpx
from fastapi import APIRouter, HTTPException
from navimoderator.backend.nodes.navimoderator import NaviModerator


llm_name = "llm_name"   #TODO: frontendの情報を反映できるようにする
compute_env = "browser"
is_translation = True
is_moderation = True


router = APIRouter()
navi_moderator = NaviModerator(
    llm_name=llm_name, 
    compute_env=compute_env, 
    is_translation=is_translation, 
    is_moderation=is_moderation, 
).build_graph()

@router.post("/moderate")
async def moderate_comments(payload: dict):
    """
    Twitch APIからコメントや推論結果を受け取って、
    LangGraphワークフローを実行する。
    """
    
    result = navi_moderator.invoke(payload)
    comments = result["comments"]

    return {
        "comments": comments
    }


