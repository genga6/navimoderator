import httpx
from fastapi import APIRouter, HTTPException
from ..nodes.navimoderator import NaviModerator, NaviModeratorState

router = APIRouter()
navi_moderator = NaviModerator().build_graph()

@router.get("/process_comment")
async def process_comment_endpoints(
    streamer_login: str, 
    access_token: str, 
    refresh_token: str, 
    comments: str,
    user_id: str, 
    action: str
    ):
    try:
        state = NaviModeratorState(
            streamer_login=streamer_login,
            access_token=access_token,
            refresh_token=refresh_token,
            comment=comments,
            user_id=user_id,
            action=action
        )
        result = await navi_moderator.invoke(state)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))