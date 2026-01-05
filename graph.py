"""
Graph construction for the influencer outreach workflow.
Refactored to match the Figma diagram with loop-based stage processing.

Architecture:
                                    START
                                      │
                                      ▼
                            ┌─────────────────┐
                            │  initialization │
                            └────────┬────────┘
                                     │
              ┌──────────────────────┴──────────────────────┐
              │                                              │
              │    ╔════════════════════════════════════╗   │
              │    ║     STAGE PROCESSING LOOP          ║   │
              │    ╚════════════════════════════════════╝   │
              │                                              │
              │         ┌─────────────────────┐             │
              │         │   stage_processor   │◄────────────┼───┐
              │         │   (基本流程节点)     │             │   │
              │         └──────────┬──────────┘             │   │
              │                    │                        │   │
              │                    ▼                        │   │
              │         ┌─────────────────────┐             │   │
              │         │     decorator       │             │   │
              │         │   (回复内容打磨)     │             │   │
              │         └──────────┬──────────┘             │   │
              │                    │                        │   │
              │                    ▼                        │   │
              │         ┌─────────────────────┐             │   │
              │         │   await_response    │             │   │
              │         │    (等待回复)        │             │   │
              │         └──────────┬──────────┘             │   │
              │                    │                        │   │
              │                    ▼                        │   │
              │         ┌─────────────────────┐             │   │
              │         │      decoder        │             │   │
              │         │    (解码节点)        │             │   │
              │         └──────────┬──────────┘             │   │
              │                    │                        │   │
              │                    ▼                        │   │
              │         ┌─────────────────────┐             │   │
              │         │   response_check    │             │   │
              │         │   (回复检查节点)     │             │   │
              │         └──────────┬──────────┘             │   │
              │                    │                        │   │
              │       ┌────────────┼────────────┐           │   │
              │       ▼            ▼            ▼           │   │
              │   continue    question     escalation       │   │
              │       │       handler       (博主⭐)        │   │
              │       │           │            │            │   │
              │       │           └────────────┘            │   │
              │       │                  │                  │   │
              │       ▼                  ▼                  │   │
              │   ┌─────────────────────────────┐           │   │
              │   │       advance_stage         │           │   │
              │   │       (推进阶段)             │           │   │
              │   └──────────────┬──────────────┘           │   │
              │                  │                          │   │
              │         ┌───────┴───────┐                   │   │
              │         ▼               ▼                   │   │
              │    more stages    all complete              │   │
              │         │               │                   │   │
              │         └───────────────┼───────────────────┘   │
              │                         │                       │
              └─────────────────────────┼───────────────────────┘
                                        │
                                        ▼
                                       END
"""

from langgraph.graph import StateGraph, START, END
from mcnagent.langgraph.state import State
from mcnagent.langgraph.nodes.other_nodes.nodes import (
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
)
from mcnagent.langgraph.nodes.other_nodes.initialization import initialization


# ============================================================================
# GRAPH CONSTRUCTION - Loop-Based Architecture
# ============================================================================

graph_builder = StateGraph(State)

# ========== ADD NODES ==========

# Initialization
graph_builder.add_node("initialization", initialization)

# Stage processing loop nodes
graph_builder.add_node("stage_processor", stage_processor)  # 基本流程节点
graph_builder.add_node("decorator", decorator)               # 回复内容打磨
graph_builder.add_node("await_response", await_response)     # 等待回复
graph_builder.add_node("decoder", decoder)                   # 解码节点
graph_builder.add_node("response_check", response_check)     # 回复检查节点

# Branching handlers
graph_builder.add_node("question_handler", question_handler)  # 问题处理节点
graph_builder.add_node("human_escalation", human_escalation)  # 人工介入节点 (博主⭐)

# Stage advancement
graph_builder.add_node("advance_stage", advance_stage)        # 推进阶段节点


# ========== ADD EDGES ==========

# Entry: START → Initialization → Stage Processor
graph_builder.add_edge(START, "initialization")
graph_builder.add_edge("initialization", "stage_processor")

# Main processing chain (per stage)
graph_builder.add_edge("stage_processor", "decorator")
graph_builder.add_edge("decorator", "await_response")
graph_builder.add_edge("await_response", "decoder")
graph_builder.add_edge("decoder", "response_check")

# Response check branching (decision diamond)
graph_builder.add_conditional_edges(
    "response_check",
    conditional_response_check,
    {
        "continue": "advance_stage",           # 正常情况 → continue
        "question_handler": "question_handler", # 博主询问问题 → question
        "human_escalation": "human_escalation", # 不确定的事情 → 博主(human)
    }
)

# Question handler and human escalation both go to advance_stage
graph_builder.add_edge("question_handler", "advance_stage")
graph_builder.add_edge("human_escalation", "advance_stage")

# Advance stage routing (loop back or end)
graph_builder.add_conditional_edges(
    "advance_stage",
    conditional_advance_stage,
    {
        "continue": "stage_processor",  # Loop back for next stage
        "end": END,                      # Workflow complete
    }
)


# ============================================================================
# GRAPH COMPILATION
# ============================================================================

def build_graph() -> StateGraph:
    """Return the configured graph builder."""
    return graph_builder


def get_graph_visualization():
    """Get the graph for visualization."""
    return graph_builder


def compile_graph():
    """Compile and return the executable graph."""
    return graph_builder.compile()
