import os
import asyncio
import logging
from typing import AsyncIterator
from navimoderator.backend.core.node import Node
from navimoderator.backend.nodes.comment_retriever.base_retriever_node import BaseRetrieverNode
from twitchio.client import Client
from twitchio.ext import commands

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TwitchRetrieverNode(Node, BaseRetrieverNode):
    def __init__(
        self,
        input_key: list[str],
        output_key: list[str],
    ):
        super().__init__(input_key, output_key)
        self.client: Client = None
        self._streamer_id: str = None
        self._access_token: str = None
        self._is_connecting: bool = False
        self._comment_task: asyncio.Task = None
        self._current_comment_queue: asyncio.Queue[dict] = asyncio.Queue(maxsize=1000)

    def _get_access_token(self):
        token = os.environ.get("TWITCH_ACCESS_TOKEN")
        if not token:
            raise ValueError("Twitch access token not found in environment variables.")
        return token

    async def _initialize_client(self) -> None:
        """TwitchIO Clientを初期化し、イベントハンドラをセットアップする。"""
        if not self.client:
            self._access_token = self._get_access_token()
            self.client = Client(token=self._access_token)

            @self.client.event()    
            async def event_ready():    
                logger.info("Twitch client ready!")

            @self.client.event()
            async def event_message(message):
                if message.echo:
                    return
                comment_data = {
                    "id": message.id, 
                    "author": message.author.name, 
                    "content": message.content, 
                    "timestamp": message.timestamp.isoformat(), 
                    "channel": message.channel.name, 
                } 
                if self._current_comment_queue.full():
                    logger.warning("Comment queue is full, dropping oldest comment.")
                    self._current_comment_queue.get_nowait()
                self._current_comment_queue.put_nowait(comment_data)

    async def _connect_and_listen(self, streamer_id: str):
        """Twitchに接続し、指定されたチャンネルのコメントを監視するタスク"""
        if not self.client:
            logger.warning("Twitch client is not initialized.")
            return
        if self._streamer_id == streamer_id:
            logger.info(f"Already connected to channel: {streamer_id}")
            return 
        if self._is_connecting:
            logger.info("Already connecting to Twitch.")
            return

        self._is_connecting = True
        try:
            if not self.client.is_connected:
                await self.client.connect()
            if self._streamer_id and self._streamer_id != streamer_id:
                await self.client.part_channels([self._streamer_id])
            
            await self.client.join_channels([streamer_id])
            self._streamer_id = streamer_id
            logger.info(f"Connected to and listening on Twitch channel: {streamer_id}")
            await self.client.start()

        except Exception as e:
            logger.error(f"Error connecting to Twitch: {e}")    # TODO: エラーからの再接続ロジックが欲しい
        finally:
            self._is_connecting = False

    async def _fetch_comments(self) -> AsyncIterator[dict]:
        """コメントキューからコメントを取得する"""
        while True:
            try:
                yield self._current_comment_queue.get_nowait()
            except asyncio.QueueEmpty:
                await asyncio.sleep(0.1)

    async def execute(self, state) -> dict:
        streamer_id = state.get(self.input_key[0])
        if not streamer_id:
            logger.error("stream_id not found in state.")
            return {}

        await self._initialize_client()

        if self._comment_task is None or self._streamer_id != streamer_id:
            if self._comment_task and not self._comment_task.done():
                self._comment_task.cancel()
                try:
                    await self._comment_task
                except asyncio.CancelledError:
                    pass
                self._comment_task = asyncio.create_task(self._connect_and_listen(streamer_id))

        comments = state.get(self.output_key[0], {})
        async for comment_data in self._fetch_comments():
            comments[comment_data["id"]] = comment_data

        return {self.output_key[0]: comments}