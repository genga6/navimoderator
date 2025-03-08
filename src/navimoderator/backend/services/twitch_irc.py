import os
import asyncio
import httpx
import websockets

TWITCH_BOT_USERNAME = os.getenv("TWITCH_MODERATOR_USERNAME")
TWITCH_IRC_URI = "wss://irc-ws.chat.twitch.tv:443"


class TwitchIRC:
    def __init__(self, streamer_login: str, access_token: str):
        self.access_token = access_token
        self.streamer_login = streamer_login
        self.websocket = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
    
    async def connect_to_chat(self):
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

    async def listen_chat(self):
        try:
            while True:
                response = await self.websocket.recv()
                if response.startswith("PING"):
                    await self.websocket.send("PONG :tmi.twitch.tv")
                else:
                    parsed_comment = self.parse_twitch_message(response)
                    if parsed_comment:
                        await self.send_comment_to_fastapi(parsed_comment)
        except websockets.ConnectionClosed:
            print("Connection lost. Reconnecting...")
            await self.reconnect_to_chat()
        except Exception as e:
            print(f"Error: {e}")
            await self.reconnect_to_chat()

    def parse_twitch_message(self, message: str):
        """
        Twitch の IRC メッセージを解析し、コメント情報を取得
        例: ":user!user@user.tmi.twitch.tv PRIVMSG #channel :message"
        """
        try:
            if "PRIVMSG" in message:
                parts = message.split("PRIVMSG")
                user_name = parts[0].split("!")[0].strip(":")  # コメント投稿者
                chat_message = parts[1].split(":", 1)[1].strip()  # コメント内容
                return {
                    "user": user_name,
                    "message": chat_message
                }
        except Exception as e:
            print(f"Failed to parse message: {message}, error: {e}")
            return None

    async def send_comment_to_fastapi(self, parsed_comment: dict):
        """
        Twitch のコメントを `fast_api/comments.py` の `/process_comment` に送信
        """
        api_url = "http://localhost:8000/process_comment"
        payload = {
            "comment": parsed_comment["message"],
            "streamer_login": self.streamer_login,
            "user_id": parsed_comment["user"],
            "access_token": self.access_token
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(api_url, json=payload)
                if response.status_code == 200:
                    print(f"Comment processed: {parsed_comment['message']}")
                else:
                    print(f"Failed to send comment to FastAPI: {response.text}")
        except Exception as e:
            print(f"Failed to send comment to FastAPI: {e}")

    async def send_message(self, message: str):
        if self.websocket:
            chat_command = f"PRIVMSG #{self.streamer_login} :{message}"
            await self.websocket.send(chat_command)
            print(f"Sent message to #{self.streamer_login}: {message}")

    async def reconnect_to_chat(self):
        if self.reconnect_attempts < self.max_reconnect_attempts:
            self.reconnect_attempts += 1
            wait_time = 2 ** self.reconnect_attempts
            print(f"Reconnecting in {wait_time} seconds...")
            await asyncio.sleep(wait_time)
            await self.connect_to_chat()
        else:
            print("Max reconnect attempts reached. Stopping reconnection.")

    async def disconnect_from_chat(self):
        if self.websocket:
            await self.websocket.close()
            print(f"Disconnected from #{self.streamer_login}")