import json
from pydantic import BaseModel


class LLMOutput(BaseModel):
    pass

class ProcessNode:
    def __init__(self):
        pass

    # def _call_llm(self, prompt: str, inference_result: str) -> Optional[LLMOutput]:
    #     """
    #     ブラウザ(ONNX Runtime Web)で推論した結果を
    #     inference_result (JSON文字列) としてサーバーが受け取り、
    #     それをパースして返すだけのメソッドに変更。
        
    #     :param prompt: 元のコメントなど
    #     :param inference_result: ブラウザ推論結果 (JSON文字列) 
    #     :return: LLMOutput（pydanticで定義した構造体） or None
    #     """
    #     try:
    #         data = json.loads(inference_result)
    #         result = LLMOutput(*data)
    #         return result
    #     except Exception as e:
    #         print(f"Error parsing inference result: {e}")
    #         return None

    def execute(self, preprocessed_comments: list) -> list:
        processed_comments = preprocessed_comments
        print("Processing of comments has been completed.")
        return processed_comments