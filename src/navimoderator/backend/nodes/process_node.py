import json
from pydantic import BaseModel


class LLMOutput(BaseModel):
    pass

class ProcessNode:
    def __init__(self):
        pass

    # def _call_llm(self, prompt: str, inference_result: str) -> Optional[LLMOutput]:
    #     """
    #     ブラウザ(ONNX Runtime Web)で推論した結果をサーバーが受け取り、
    #     それをパースして返すだけのメソッドに変更。
    #     
    #     
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

    def execute(self, preprocessed_comments: list[dict]) -> list[dict]:

        # ONNX Runtime Webで推論した結果（ダミーデータ）
        processed_comments = [
            {
            "timestamp": "2025-03-14T12:34:56Z", 
            "user_name": "@someone_in_chat", 
            "comment_id": "xxxx", 
            "comment": "Hello!", 
            "translated_text": "こんにちは!",
	        "is_harassment": False,  
            }, 
            {
            "timestamp": "2025-03-14T12:34:56Z", 
            "user_name": "@someone_in_chat", 
            "comment_id": "xxxx", 
            "comment": "これは誹謗中傷コメントです", 
            "translated_text": "",
	        "is_harassment": True,  
            }, 
        ]
        print("Processing of comments has been completed.")
        return processed_comments