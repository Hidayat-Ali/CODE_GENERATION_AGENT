from langgraph.graph import StateGraph, END

from agent.state import AgentState
from agent.nodes import (
    generate_code_node,
    planner_node,
    review_code_node,
    fix_code_node,
    save_code_node,
    route_after_review_node
)

builder = StateGraph(AgentState)

builder.add_node(
    "planner",
    planner_node
)
builder.add_node(
    "generate_code",
    generate_code_node
)

builder.add_node(
    "review_code",
    review_code_node
)

builder.add_node(
    "fix_code",
    fix_code_node
)

builder.add_node(
    "save_code",
    save_code_node
)

builder.set_entry_point(
    "planner"
)
builder.add_edge(
    "planner",
    "generate_code"
)
builder.add_edge(
    "generate_code",
    "review_code"
)

builder.add_conditional_edges(
    "review_code",
    route_after_review_node
)

builder.add_edge(
    "fix_code",
    "save_code"
)

builder.add_edge(
    "save_code",
    END
)

graph = builder.compile()