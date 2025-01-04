import pytest
from navimoderator.backend.nodes.user_progress_node import UserProgressNode
from langgraph.graph import StateGraph
from typing import TypedDict
from freezegun import freeze_time


class State(TypedDict):
    user_progress_raw: str
    stream_start_time: str
    cumulative_play_time: str
    final_play_time_range: str
    

def test_user_progress_node():
    input_key = ["user_progress_raw", "stream_start_time", "cumulative_play_time"]
    output_key = ["final_play_time_range"]

    graph_builder = StateGraph(State)
    graph_builder.add_node(
        "user_progress_node",
        UserProgressNode(
            input_key=input_key,
            output_key=output_key,
        ),
    )
    graph_builder.set_entry_point("user_progress_node")
    graph_builder.set_finish_point("user_progress_node")
    graph = graph_builder.compile()

    with freeze_time("2025-01-02T16:00:00"):
        test_cases = [
            {
                "name": "Valid input with user progress",
                "state": {
                    "user_progress_raw": "5-10",
                    "stream_start_time": "2025-01-02T14:00:00",
                    "cumulative_play_time": "10-15",
                },
                "expected": {"final_play_time_range": "7-12時間"},  # Assume 2 hours have passed
            },
            {
                "name": "No user progress, use cumulative",
                "state": {
                    "user_progress_raw": None,
                    "stream_start_time": "2025-01-02T14:00:00",
                    "cumulative_play_time": "10-15",
                },
                "expected": {"final_play_time_range": "12-17時間"},  # Assume 2 hours have passed
            },
            {
                "name": "Invalid stream start time",
                "state": {
                    "user_progress_raw": "5-10",
                    "stream_start_time": "invalid-time",
                    "cumulative_play_time": "10-15",
                },
                "expected_exception": ValueError,
            },
            {
                "name": "No progress data at all",
                "state": {
                    "user_progress_raw": None,
                    "stream_start_time": "2025-01-02T14:00:00",
                    "cumulative_play_time": None,
                },
                "expected": {"final_play_time_range": None},
            },
        ]

        for case in test_cases:
            if "expected_exception" in case:
                with pytest.raises(case["expected_exception"], match=".*"):
                    graph.invoke(case["state"], debug=True)
            else:
                result_state = graph.invoke(case["state"], debug=True)
                assert result_state["final_play_time_range"] == case["expected"]["final_play_time_range"], f"Failed on case: {case['name']}"