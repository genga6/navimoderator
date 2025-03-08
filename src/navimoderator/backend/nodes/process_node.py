import re
import json
from pydantic import BaseModel
from jinja2 import Template, Environment
from litellm import completion


class LLMOutput(BaseModel):
    pass

class ProcessNode:
    def init(self, llm_name: str):
        self.llm_name = llm_name

    def _call_llm(self, prompt: str, max_retries: int = 3) -> str:
        for attempt in range(max_retries): 
            try:
                response = completion(
                    model=self.llm_name,
                    messages=[
                        {"role": "user", "content": prompt},
                    ],
                    response_format=LLMOutput,
                )
                structured_output = json.loads(response.choices[0].message.content)
                return structured_output[""]
            except Exception as e:
                print(f"[Attempt {attempt+1}/{max_retries}] Unexpected error: {e}")
        print("Exceeded maximum retries for LLM call.")
        return None