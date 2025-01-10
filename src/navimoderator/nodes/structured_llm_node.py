import ast
from navimoderator.backend.core.node import Node
from litellm import completion
from jinja2 import Environment
from pydantic import BaseModel, create_model


class DynamicModel(BaseModel):
    pass


class StructuredLLMNode(Node):
    def __init__(
        self,
        input_key: list[str],
        output_key: list[str],
        llm_name: str,
        prompt_template: str,
    ):
        super().__init__(input_key, output_key)
        self.llm_name = llm_name
        self.prompt_template = prompt_template
        self.dynamicmodel = self._create_dynamic_model(DynamicModel)

    def _create_dynamic_model(self, base_model: BaseModel):
        default_type = str
        default_required = ...
        fields = {field: (default_type, default_required) for field in self.output_key}
        return create_model(
            base_model.__name__,
            **fields,
            __base__=base_model,
        )

    def litellm_output(self, llm_name: str, prompt: str, response_field) -> dict:
        response = completion(
            model=llm_name,
            messages=[
                {"role": "user", "content": prompt},
            ],
            response_format=response_field,
        )
        output = response.choices[0].message.content
        output_dict = ast.literal_eval(output)
        return output_dict

    def execute(self, state) -> dict:
        data = {key: state[key] for key in self.input_key}

        env = Environment()
        template = env.from_string(self.prompt_template)
        prompt = template.render(data)

        result_dict = {}
        if self.llm_name == "gpt-4o":    #TODO: Expand the model
            result_dict = self.litellm_output(self.llm_name, prompt, self.dynamicmodel)
        elif self.llm_name == "gpt-3.5-turbo":
            result_dict = self.litellm_output(self.llm_name, prompt, self.dynamicmodel)
        else:
            raise ValueError("LLM not supported")
            
        return {**result_dict}