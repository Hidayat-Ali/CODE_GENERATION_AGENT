from langgraph.graph import StateGraph, END

from agent.state import AgentState
from agent.nodes import generate_code_node,review_code_node, save_code_node


builder = StateGraph(AgentState)

builder.add_node(
    "generate_code",
    generate_code_node
)

builder.add_node(
    "review_code",
    review_code_node
)

builder.add_node(
    "save_code",
    save_code_node
)

builder.set_entry_point(
    "generate_code"
)

builder.add_edge(
    "generate_code",
    "review_code"
)

builder.add_edge(
    "save_code",
    END
)

graph = builder.compile()