import hashlib
import re
import time
import emoji
import MeCab
from navimoderator.backend.core.node import Node
# from transformers import pipeline
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed


class CommentFilterNode(Node):
    frequent_comment = Counter()  

    def __init__(self, input_key: list[str], output_key: list[str]):
        super().__init__(input_key, output_key)
        # self.model = pipeline("zero-shot-classification", model="cl-tohoku/bert-base-japanese")
        self.mecab = MeCab.Tagger("-Owakati")
        self.last_update_time = time.time()
        self.update_interval = 600
        self.cache = defaultdict(dict)

    def execute(self, state) -> dict:
        comments = [{"text": comment} for comment in state[self.input_key[0]]]
        self._update_frequent_comments(comments)

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self._process_comment, comment): idx for idx, comment in enumerate(comments)}
            
            for future in as_completed(futures):
                idx = futures[future]
                result = future.result()
                comments[idx]["is_spoiler"] = result["is_spoiler"]
        
        return {self.output_key[0]: comments}
    
    def _update_frequent_comments(self, comments: list):
        current_time = time.time()
        if current_time - self.last_update_time > self.update_interval:
            self.last_update_time = current_time
            self.frequent_comment.update(comments)
       
    def _process_comment(self, comment: dict) -> dict:
        is_spoiler = self._is_never_spoiler(comment)

        """
        if not is_spoiler:
            result = self.model(comment, candidate_labels=["spoiler", "non-spoiler"])
            is_spoiler = result['labels'][0] == "spoiler"
        """
        return {'comment': comment, 'is_spoiler': is_spoiler}
    
    def _is_never_spoiler(self, comment: dict) -> bool:
        cache_key = self._generate_cache_key(comment["text"])

        if self._is_emoji_only(comment, cache_key):
            return True
        if self._is_frequent_comment(comment, cache_key):
            return True
        if self._is_repeated_pattern(comment, cache_key):
            return True
        return False

    def _is_emoji_only(self, comment: dict, cache_key: str) -> bool:
        if cache_key in self.cache:
            return self.cache[cache_key].get("is_emoji_only", False)
        
        text_without_emoji = emoji.replace_emoji(comment, replace="")
        result = not text_without_emoji.strip() and all(re.fullmatch(r"(:[a-zA-Z0-9_]+:)", part) for part in comment.split())
        self.cache[cache_key] = {"is_emoji_only": result}
        return result

    """
    def _is_short_comment(self, comment: str, max_words=3, max_length=10) -> bool:
        words = self.mecab.parse(comment).split()
        return len(words) <= max_words or len(comment) <= max_length  # TODO: 何単語、何文字がいいかは要検討
    """
    
    def _is_frequent_comment(self, comment: str, cache_key: str, frequent=2) -> bool:
        if cache_key in self.cache:
            return self.cache[cache_key].get("is_frequent_comment", False)

        frequent_count = self.frequent_comment[comment]
        result = frequent_count > frequent
        self.cache[cache_key] = {"is_frequent_comment": result}
        return result
    
    def _is_repeated_pattern(self, comment: str, cache_key: str) -> bool:
        if cache_key in self.cache:
            return self.cache[cache_key].get("is_repeated_pattern", False)
        
        result = bool(re.fullmatch(r"(.)\1{2,}", comment))
        self.cache[cache_key] = {"is_repeated_pattern": result}
        return result
    
    def _generate_cache_key(self, comment: str) -> str:
        return hashlib.md5(comment.encode('utf-8')).hexdigest()