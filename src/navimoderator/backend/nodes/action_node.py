class ActionNode:
    # 明らかにLLMで処理する必要のないコメントを特定（絵文字だけのコメントなど）
    # ただし、連投コメントをどう対応するかは要検討
    def __init__(self):
        pass

    def execute(self, processed_comments: list) -> str:
        action = "pass"
        print("Action has been determined.")
        return action