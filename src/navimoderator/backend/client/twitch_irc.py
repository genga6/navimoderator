import os
import asyncio
import httpx
import websockets
import time

TWITCH_BOT_USERNAME = os.getenv("TWITCH_MODERATOR_USERNAME")
TWITCH_IRC_URI = "wss://irc-ws.chat.twitch.tv:443"


class TwitchIRC:
    """
    Twtich IRC サーバーへクライアントして接続し、
    チャットメッセージを受け取る機能
    """
    def __init__(self, streamer_login: str, access_token: str, refresh_token: str):
        self.streamer_login = streamer_login
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.websocket = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
    
    # --- 接続関連 ---
    async def connect_to_chat(self) -> None:
        try:
            self.websocket = await websockets.connect(TWITCH_IRC_URI)
            await self.websocket.send(f"PASS oauth:{self.access_token}")
            await self.websocket.send(f"NICK {TWITCH_BOT_USERNAME}")
            await self.websocket.send(f"JOIN #{self.streamer_login}")

            print(f"Connected to Twitch chat: #{self.streamer_login}")
            self.reconnect_attempts = 0
            await self.listen_chat()
        except Exception as e:
            print(f"Failed to connect to Twitch chat: {e}")
            await self.reconnect_to_chat()

    async def reconnect_to_chat(self) -> None:
        if self.reconnect_attempts < self.max_reconnect_attempts:
            self.reconnect_attempts += 1
            wait_time = 2 ** self.reconnect_attempts
            print(f"Reconnecting in {wait_time} seconds...")
            await asyncio.sleep(wait_time)
            await self.connect_to_chat()
        else:
            print("Max reconnect attempts reached. Stopping reconnection.")

    async def disconnect_from_chat(self) -> None:
        if self.websocket:
            await self.websocket.close()
            print(f"Disconnected from #{self.streamer_login}")

    # --- メッセージ関連 ---
    async def listen_chat(self) -> None:
        try:
            while True:
                response = await self.websocket.recv()
                if response.startswith("PING"):
                    await self.websocket.send("PONG :tmi.twitch.tv")
                else:
                    parsed_message = self.parse_twitch_message(response)
                    if parsed_message:
                        await self.send_comment_to_fastapi(parsed_message)
        except websockets.ConnectionClosed:
            print("Connection lost. Reconnecting...")
            await self.reconnect_to_chat()
        except Exception as e:
            print(f"Error: {e}")
            await self.reconnect_to_chat()

    def parse_twitch_message(self, message: str) -> Optional[dict]:
        """
        Twitch の IRC メッセージを解析し、コメント情報を取得
        例: 
        ```
        @badge-info=;badges=;color=...;id=abcd1234;tmi-sent-ts=1710412345678 :foo!foo@foo.tmi.twitch.tv PRIVMSG #bar :Hello!
        ```
        """
        try:
            if message.startswith("@"):
                tag_part, irc_part = message.split(" ", 1)
                tags = {k: v for k, v in [kv.split("=") for kv in tag_part[1:].split(";") if "=" in kv]}
            else:
                tags = {}
            
            if "PRIVMSG" in irc_part:
                parts = irc_part.split("PRIVMSG")
                user_name = parts[0].split("!")[0].strip(":")  # コメント投稿者
                comment = parts[1].split(":", 1)[1].strip()  # コメント内容

                comment_id = tags.get("id", "")
                timestamp = time.strftime(
                    "%Y-%m-%dT%H:%M:%SZ",
                    time.gmtime(int(tags.get("tmi-sent-ts", "0")) / 1000)
                )

                return {
                    "timestamp": timestamp,
                    "user_name": user_name,
                    "comment_id": comment_id,
                    "comment": comment
                }

        except Exception as e:
            print(f"Failed to parse message: {message}, error: {e}")
            return None

    async def send_comment_to_fastapi(self, parsed_message: dict):
        """
        Twitch のコメントを `fast_api/comments_router.py` の `/moderate` に送信
        """
        api_url = "http://localhost:8000/moderate"
        payload = {
            "streamer_login": self.streamer_login,
            "access_token": self.access_token, 
            "refresh_token": self.refresh_token, 
            "timestamp": parsed_message["timestamp"],
            "user_name": parsed_message["user_name"],
            "comment_id": parsed_message["comment_id"],
            "comment": parsed_message["comment"],
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(api_url, json=payload) # TODO: パッチ処理にする（現状は1コメントずつLangGraphが回る）
                if response.status_code == 200:
                    print(f"Comment processed: {parsed_message['comment']}")
                else:
                    print(f"Failed to send comment to FastAPI: {response.text}")
        except Exception as e:
            print(f"Failed to send comment to FastAPI: {e}")

    async def send_message(self, message: str):
        if self.websocket:
            chat_command = f"PRIVMSG #{self.streamer_login} :{message}"
            await self.websocket.send(chat_command)
            print(f"Sent message to #{self.streamer_login}: {message}")