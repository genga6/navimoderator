import os
from navimoderator.backend.core.node import Node
from navimoderator.backend.nodes.comment_retriever.base_retriever_node import BaseRetrieverNode
from googleapiclient.discovery import build

class YoutubeRetrieverNode(Node, BaseRetrieverNode):
    def __init__(
        self, 
        input_key: list[str], 
        output_key: list[str],
    ):
        super().__init__(input_key, output_key)
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.youtube_api_key:
            raise ValueError("YOUTUBE_API_KEY is not set in the environment variables")
        
    def _fetch_comments(self, video_id: str) -> list[str]:
        youtube = build("youtube", "v3", developerKey=self.youtube_api_key)

        video_response = youtube.videos().list(
            part="liveStreamingDetails",
            id=video_id
        ).execute()
        live_details = video_response["items"][0]["liveStreamingDetails"]
        live_chat_id = live_details["activeLiveChatId"]

        comments_response = youtube.liveChatMessages().list(
            liveChatId=live_chat_id,
            part="snippet, authorDetails",
            maxResults=200, 
        ).execute()

        comments = []
        for item in comments_response["items"]:
            comment = item["snippet"]["displayMessage"]
            comments.append(comment)
        return comments
    
    def _process_comments(self, comments: list) -> list[str]:
        return comments

    def execute(self, state) -> dict:
        video_id = state[self.input_key[0]]
        comments = self._fetch_comments(video_id)
        processed_comments = self._process_comments(comments)
        state[self.output_key[0]] = processed_comments
        return state