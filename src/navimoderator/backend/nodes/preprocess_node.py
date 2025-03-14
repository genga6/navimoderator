class PreprocessNode:
    # 明らかにLLMで処理する必要のないコメントを特定（絵文字だけのコメントなど）
    # ただし、連投コメントをどう対応するかは要検討
    def __init__(self):
        pass

    def execute(self, comments: list[dict]) -> list[dict]:
        preprocessed_comments = comments
        print("Pre-processing of comments has been completed.")
        return preprocessed_comments