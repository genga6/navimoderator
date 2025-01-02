import pytest
from spoilbuster.backend.nodes.comment_listener.youtube_listener_node import YoutubeListenerNode
from langgraph.graph import StateGraph
from typing import TypedDict
from unittest.mock import patch

class State(TypedDict):
    video_id: str
    processed_comments: list[str]
    

@pytest.fixture
def mock_youtube_listener():
    with patch("spoilbuster.backend.nodes.comment_listener.youtube_listener_node.YoutubeListenerNode._fetch_comments") as mock_fetch:
        mock_fetch.return_value = [
            "This is a test comment.",
            "Another test comment."
        ]
        yield mock_fetch

def test_youtube_listener_node(mock_youtube_listener):
    input_key = ["video_id"]
    output_key = ["processed_comments"]

    graph_builder = StateGraph(State)
    graph_builder.add_node(
        "youtube_listener_node",
        YoutubeListenerNode(
            input_key=input_key,
            output_key=output_key,
        ),
    )
    graph_builder.set_entry_point("youtube_listener_node")
    graph_builder.set_finish_point("youtube_listener_node")
    graph = graph_builder.compile()

    state = {
        "video_id": "test_video_id",
    }
    result_state = graph.invoke(state, debug=True)

    assert "processed_comments" in result_state, "Messages key should exist in the result state."
    assert len(result_state["processed_comments"]) == 2, "There should be 2 messages in the result."
    assert result_state["processed_comments"][0] == "This is a test comment."
    assert result_state["processed_comments"][1] == "Another test comment."