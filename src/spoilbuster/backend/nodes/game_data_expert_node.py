from spoilbuster.backend.core.node import Node

class GameDataExpertNode(Node):
    def __init__(
        self, 
        input_key: list[str], 
        output_key: list[str],
    ):
        super().__init__(input_key, output_key)

    def _extract_features(self, game_data: str) -> dict:
        pass    #TODO: ゲームデータから特徴量を抽出するロジック（軽量処理）

    def execute(self, state) -> dict:
        game_data = state[self.input_key[0]]
        
        return {   
            self.output_key[0]: self._extract_features(game_data),
        }