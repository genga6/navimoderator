import sqlite3
from spoilbuster.backend.core.node import Node

class GameDataNode(Node):
    def __init__(
        self, 
        input_key: list[str], 
        output_key: list[str],
        db_path: str,
    ):
        super().__init__(input_key, output_key)
        self.db_path = db_path

    def _fetch_game_info(self, game_title: str) -> dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = "SELECT title, description, raw_data FROM game_data WHERE title = ?"
        cursor.execute(query, (game_title,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"title": row[0], "description": row[1], "raw_data": row[2]}
        return None

    def _generate_keywords(self, game_info: dict) -> list[str]:
        description_keywords = game_info.get("description", "").split()
        raw_data_keywords = str(game_info.get("raw_data", "")).split()
        return list(set(description_keywords + raw_data_keywords))  # 重複排除

    def _flag_comments(self, youtube_comments: list[str], game_keywords: list[str]) -> list[str]:
        flagged_comments = []
        for comment in youtube_comments:
            flagged = any(keyword in comment for keyword in game_keywords)
            flagged_comments.append({"comment": comment, "flagged": flagged})
        return flagged_comments

    def execute(self, state) -> dict:
        youtube_comments = state[self.input_key[0]]
        game_title = state[self.input_key[1]]

        game_info = self._fetch_game_info(game_title)
        if not game_info:
            raise ValueError(f"Game info not found for {game_title}")
        
        game_keywords = self._generate_keywords(game_info)
        flagged_comments = self._flag_comments(youtube_comments, game_keywords)
        
        return {   
            self.output_key[0]: flagged_comments,
            self.output_key[1]: game_info,
        }