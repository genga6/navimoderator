
from spoilbuster.backend.core.node import Node

class GameDataNode(Node):
    def __init__(
        self, 
        input_key: list[str], 
        output_key: list[str],
    ):
        super().__init__(input_key, output_key)


    def execute(self, state) -> dict:
        pass    #TODO: DBのやり取りを通じて、「ゲームに関するコメントにフラグ」「ゲーム情報を提供」を担う