from spoilbuster.backend.core.node import Node

class GameDataNode(Node):
    def __init__(
        self, 
        input_key: list[str], 
        output_key: list[str],
    ):
        super().__init__(input_key, output_key)

    def _fetch_game_data(self, game_title: str) -> dict:
        pass    #TODO: 外部APIから情報取得する

    def execute(self, state) -> dict:
        game_title = state[self.input_key[0]]

        game_info = self._fetch_game_data(game_title)
        if not game_info:
            raise ValueError(f"Game info not found for {game_title}")
        
        return {   
            self.output_key[0]: self._fetch_game_data(game_title),
            self.output_key[1]: game_info,
        }