import pytest
from navimoderator.backend.nodes.spoiler_detection.content_data_node import ContentDataNode
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    content_title: str
    content_data: dict
    

def test_content_data_node():
    input_key = ["content_title"]
    output_key = ["content_data"]

    graph_builder = StateGraph(State)
    graph_builder.add_node(
        "content_data_node",
        ContentDataNode(
            input_key=input_key,
            output_key=output_key,
        ),
    )
    graph_builder.set_entry_point("content_data_node")
    graph_builder.set_finish_point("content_data_node")
    graph = graph_builder.compile()