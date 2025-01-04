import pytest
from navimoderator.backend.nodes.comment_filter_node import CommentFilterNode
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    comments: list[str]
    filtered_comments: list[dict[str, str]]
    
def test_comment_filter_node():
    input_key = ["comments"]
    output_key = ["filtered_comments"]

    test_comments = [
        "ニール死ぬよ",  # 明らかなネタバレ
        "すごい映画だった",  # ネタバレなし
        "ラストシーン感動した",  # ネタバレかもしれないが、具体的な情報は含まない
        "何が起こったのか分からない",  # ネタバレ含まず
        "あああああ", 
        "こんばんは", 
        "こんばんは", 
        "こんばんは", 
        "😭😭😭👏👏", 
    ]

    graph_builder = StateGraph(State)
    graph_builder.add_node(
        "comment_filter_node",
        CommentFilterNode(
            input_key=input_key,
            output_key=output_key,
        ),
    )
    graph_builder.set_entry_point("comment_filter_node")
    graph_builder.set_finish_point("comment_filter_node")
    graph = graph_builder.compile()

    state = State(comments=test_comments, filtered_comments=[])
    result_state = graph.invoke(state, debug=True)

    filtered_comments = result_state["filtered_comments"]

    assert len(filtered_comments) == len(test_comments)

    assert filtered_comments[0]["is_spoiler"] == True   # "ニール死ぬよ" はネタバレ
    assert filtered_comments[1]["is_spoiler"] == False  # "すごい映画だった" はネタバレではない
    assert filtered_comments[2]["is_spoiler"] == True  # "ラストシーン感動した" はネタバレかもしれないが、具体的な情報なし
    assert filtered_comments[3]["is_spoiler"] == False  # "何が起こったのか分からない" はネタバレではない
    assert filtered_comments[4]["is_spoiler"] == False
    assert filtered_comments[5]["is_spoiler"] == False
    assert filtered_comments[6]["is_spoiler"] == False
    assert filtered_comments[7]["is_spoiler"] == False
    assert filtered_comments[8]["is_spoiler"] == False 