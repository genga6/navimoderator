class ActionNode:
    def __init__(self):
        pass

    def _action_decision(self, processed_comments: list[dict]) -> list[dict]:
        for comment in processed_comments:
            if comment.get("is_harassment", False):
                comment["moderator_action"] = "delete"
            elif comment.get("translated_text"):
                comment["moderator_action"] = "post"
                comment["post_text"] = f"{comment['translated_text']} by {comment['user_name']}"
            else:
                comment["moderator_action"] = "pass"

        return processed_comments
    
    def execute(self, processed_comments: list[dict]) -> list[dict]:
        processed_comments = self._action_decision(processed_comments)
        return processed_comments
