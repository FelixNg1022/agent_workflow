"""
Node definitions for the workflow graph.
Updated for loop-based stage processing architecture.
"""

from mcnagent.langgraph.nodes.pr_nodes.pr_nodes import PR_Nodes
from mcnagent.langgraph.nodes.other_nodes.initialization import initialization
from mcnagent.langgraph.nodes.other_nodes.nodes import (
    # Main loop nodes
    stage_processor,
    decorator,
    await_response,
    decoder,
    response_check,
    conditional_response_check,
    question_handler,
    human_escalation,
    advance_stage,
    conditional_advance_stage,
    # Legacy compatibility
    determination_or_decorator,
    conditional_determination_or_decorator,
    determination,
    kol_response_test,
)

__all__ = [
    "PR_Nodes",
    # Initialization
    "initialization",
    # Main loop nodes
    "stage_processor",
    "decorator",
    "await_response",
    "decoder",
    "response_check",
    "conditional_response_check",
    "question_handler",
    "human_escalation",
    "advance_stage",
    "conditional_advance_stage",
    # Legacy compatibility
    "determination_or_decorator",
    "conditional_determination_or_decorator",
    "determination",
    "kol_response_test",
]
