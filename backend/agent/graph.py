from langgraph.graph import StateGraph, END

from agent.state import AgentState
from agent.nodes import (
    collect_context_node,
    dependency_error_node,
    execute_code_node,
    generate_code_node,
    next_file_node,
    planner_node,
    review_code_node,
    fix_code_node,
    route_after_execution_node,
    route_after_saving_node,
    save_code_node,
    route_after_review_node,
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
builder.add_node(
    "collect_context",
    collect_context_node
)
builder.add_node(   
    "next_file",
    next_file_node
)
builder.add_node(
    "execute_code",
    execute_code_node
)
builder.add_node(
    "dependency_error",
    dependency_error_node
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
    "execute_code"
)
builder.add_conditional_edges(
    "execute_code",
    route_after_execution_node
)
builder.add_conditional_edges(
    "collect_context",
    route_after_saving_node
)
builder.add_edge(
    "next_file",
    "generate_code" 
)   

graph = builder.compile()