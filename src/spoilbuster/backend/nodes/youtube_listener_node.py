import os
from spoilbuster.backend.core.node import Node
from googleapiclient.discovery import build

class YoutubeListenerNode(Node):
    def __init__(
        self, 
        input_key: list[str], 
        output_key: list[str],
    ):
        super().__init__(input_key, output_key)
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.youtube_api_key:
            raise ValueError("YOUTUBE_API_KEY is not set in the environment variables")
        
    def _fetch_live_chat_messages(self, video_id: str) -> list[str]:
        youtube = build("youtube", "v3", developerKey=self.youtube_api_key)

        video_response = youtube.videos().list(
            part="liveStreamingDetails",
            id=video_id
        ).execute()
        live_details = video_response["items"][0]["liveStreamingDetails"]
        live_chat_id = live_details["activeLiveChatId"]

        messages_response = youtube.liveChatMessages().list(
            liveChatId=live_chat_id,
            part="snippet, authorDetails",
            maxResults=200, 
        ).execute()

        messages = []
        for item in messages_response["items"]:
            message = item["snippet"]["displayMessage"]
            messages.append(message)
        return messages

    def execute(self, state) -> dict:
        video_id = state[self.input_key[0]]
        messages = self._fetch_live_chat_messages(video_id)
        state[self.output_key[0]] = messages
        return state