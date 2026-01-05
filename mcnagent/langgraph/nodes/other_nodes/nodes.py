"""
Utility nodes for response handling, routing, and decision making.
Refactored for loop-based stage processing matching the Figma diagram.

Flow per stage:
  stage_processor → decorator → await_response → decoder → response_check
                                                              ↓
                                          ┌──────────────────┼──────────────────┐
                                          ↓                  ↓                  ↓
                                      continue        question_handler   human_escalation
                                          ↓                  ↓                  ↓
                                    advance_stage ←─────────┴──────────────────┘
"""

from typing import Literal
from mcnagent.langgraph.state import State, get_next_stage, get_stage_by_index, STAGE_ORDER
from mcnagent.langgraph.nodes.pr_nodes.pr_nodes import PR_Nodes


# ============================================================================
# STAGE PROCESSOR NODE
# ============================================================================

def stage_processor(state: State) -> dict:
    """
    基本流程节点处理器
    Generic stage processor that executes the current stage's action.
    Routes to the appropriate PR_Node handler based on current_stage.
    """
    current_stage = state.get("current_stage", "greet")
    stage_index = state.get("current_stage_index", 0)
    
    print(f"\n{'='*60}")
    print(f"📍 STAGE PROCESSOR: Processing stage '{current_stage}' (index: {stage_index})")
    print(f"{'='*60}")
    
    # Get the handler for current stage
    handler = PR_Nodes.get_handler(current_stage)
    
    if handler:
        # Execute the stage handler
        result = handler(state)
        return {
            **result,
            "current_stage": current_stage,
            "current_stage_index": stage_index,
        }
    else:
        print(f"⚠️ No handler found for stage: {current_stage}")
        return {
            "stage_completed": True,
            "messages": [f"Unknown stage: {current_stage}"],
        }


# ============================================================================
# DECORATOR NODE (回复内容打磨)
# ============================================================================

def decorator(state: State) -> dict:
    """
    装饰节点 / 回复内容打磨
    Polish and refine outgoing message before sending.
    Enhances AI-generated responses for better communication.
    
    This is the central polishing hub that processes outgoing messages
    for ALL stages (matching the Figma diagram).
    """
    print("✨ [decorator] 回复内容打磨 - Polishing outgoing message...")
    
    pending_message = state.get("polished_response", "")
    current_stage = state.get("current_stage", "")
    
    # TODO: Use LLM to polish response
    # - Improve tone and professionalism
    # - Add personalization based on influencer_info
    # - Ensure cultural appropriateness
    # - Add appropriate emojis/formatting
    
    polished = pending_message  # Placeholder - would be LLM enhanced
    
    print(f"   Stage: {current_stage}")
    print(f"   Message: {polished[:50]}..." if len(polished) > 50 else f"   Message: {polished}")
    
    return {
        "polished_response": polished,
        "messages": [f"[decorator] Response polished for stage: {current_stage}"],
    }


# ============================================================================
# AWAIT RESPONSE NODE
# ============================================================================

def await_response(state: State) -> dict:
    """
    等待回复节点
    Simulates waiting for and receiving KOL response.
    In production, this would integrate with messaging platform APIs.
    """
    current_stage = state.get("current_stage", "")
    print(f"⏳ [await_response] Waiting for KOL response (stage: {current_stage})...")
    
    # TODO: In production:
    # - Send the polished_response via appropriate channel
    # - Wait for and capture KOL response
    # - Store in pending_response
    
    # Simulated response for testing
    simulated_response = f"[Simulated KOL response for {current_stage} stage]"
    
    return {
        "pending_response": simulated_response,
        "decoded_response": None,  # Clear for new decoding
        "kol_intent": None,  # Clear for new determination
        "messages": [f"[await] Response received for stage: {current_stage}"],
    }


# ============================================================================
# DECODER NODE (解码节点)
# ============================================================================

def decoder(state: State) -> dict:
    """
    解码节点
    Decode and parse influencer response into structured format.
    Extracts intent, entities, and key information.
    """
    print("🔓 [decoder] Decoding influencer response...")
    
    pending = state.get("pending_response", "")
    current_stage = state.get("current_stage", "")
    
    # TODO: Use LLM to parse and extract structured info from response
    decoded = {
        "raw_text": pending,
        "intent": None,  # Will be determined in response_check
        "entities": {},  # Extracted entities like dates, prices, addresses
        "sentiment": "neutral",  # positive, negative, neutral
        "requires_action": False,
        "has_question": False,
        "stage": current_stage,
    }
    
    # Simple keyword detection for simulation
    if pending:
        text_lower = pending.lower()
        if any(q in text_lower for q in ["?", "？", "问", "什么", "怎么", "为什么"]):
            decoded["has_question"] = True
            decoded["intent"] = "question"
        elif any(neg in text_lower for neg in ["不", "没", "拒绝", "不行", "取消"]):
            decoded["intent"] = "decline"
            decoded["sentiment"] = "negative"
        else:
            decoded["intent"] = "accept"
            decoded["sentiment"] = "positive"
    
    return {
        "decoded_response": decoded,
        "messages": [f"[decoder] Response decoded for stage: {current_stage}"],
    }


# ============================================================================
# RESPONSE CHECK NODE (回复检查节点)
# ============================================================================

def response_check(state: State) -> dict:
    """
    回复检查节点
    Analyze decoded response and prepare for routing decision.
    Determines: continue, question_handler, or human_escalation.
    """
    print("🔎 [response_check] Checking response and determining next action...")
    
    decoded = state.get("decoded_response", {})
    current_stage = state.get("current_stage", "")
    
    # Determine response type based on decoded content
    intent = decoded.get("intent", "accept") if decoded else "accept"
    has_question = decoded.get("has_question", False) if decoded else False
    sentiment = decoded.get("sentiment", "neutral") if decoded else "neutral"
    
    # Routing logic
    if intent == "accept" and not has_question:
        response_type = "continue"
    elif intent == "question" or has_question:
        response_type = "question"
    elif intent in ["decline", "negotiate"] or sentiment == "negative":
        response_type = "escalation"
    else:
        response_type = "continue"
    
    print(f"   Stage: {current_stage}")
    print(f"   Intent: {intent}")
    print(f"   Response Type: {response_type}")
    
    return {
        "kol_intent": intent,
        "response_type": response_type,
        "messages": [f"[response_check] Intent: {intent}, Route: {response_type}"],
    }


def conditional_response_check(state: State) -> Literal["continue", "question_handler", "human_escalation"]:
    """
    Conditional routing function after response_check.
    Routes based on response_type determined in response_check.
    
    This is the decision diamond in the Figma diagram:
    - 正常情况 → continue
    - 博主询问问题或者不确定的事情 → question_handler or human_escalation
    """
    response_type = state.get("response_type", "continue")
    
    if response_type == "question":
        return "question_handler"
    elif response_type == "escalation":
        return "human_escalation"
    else:
        return "continue"


# ============================================================================
# QUESTION HANDLER NODE (问题处理节点)
# ============================================================================

def question_handler(state: State) -> dict:
    """
    问题处理节点
    Handle questions from influencer.
    Attempts to resolve questions automatically before escalating.
    
    Examples:
    - 产品有什么颜色 (Product color questions)
    - 我拍露上镜妆吗 (Content style questions)
    - 档期可以调整吗 (Schedule flexibility questions)
    """
    print("❓ [question_handler] Processing influencer questions...")
    
    decoded = state.get("decoded_response", {})
    current_stage = state.get("current_stage", "")
    question_text = decoded.get("raw_text", "") if decoded else ""
    
    # TODO: Use LLM to:
    # 1. Classify question type
    # 2. Attempt to answer from knowledge base
    # 3. If unable to answer, flag for human review
    
    can_resolve = True  # Placeholder - would be determined by LLM
    
    if can_resolve:
        # Generate answer
        answer = f"[Auto-generated answer for question in {current_stage} stage]"
        print(f"   ✅ Question resolved automatically")
        return {
            "polished_response": answer,
            "has_questions": True,
            "needs_human_review": False,
            "messages": [f"[question_handler] Question resolved for stage: {current_stage}"],
        }
    else:
        # Cannot resolve - this would typically go to human_escalation
        # but for now we'll pass through
        print(f"   ⚠️ Question requires human review")
        return {
            "has_questions": True,
            "needs_human_review": True,
            "messages": [f"[question_handler] Question flagged for review: {current_stage}"],
        }


# ============================================================================
# HUMAN ESCALATION NODE (人工介入节点 / 博主节点)
# ============================================================================

def human_escalation(state: State) -> dict:
    """
    人工介入节点 (博主节点 ⭐)
    Escalate to human operator when:
    - Complex questions that AI cannot resolve
    - Confirmation required for important decisions
    - Influencer explicitly requests human contact
    - Negotiation or decline scenarios
    - Any uncertain situations
    
    This corresponds to the "博主" node with ⭐ in the Figma diagram.
    """
    print("👤 [human_escalation] ⭐ Escalating to human operator (博主节点)...")
    
    current_stage = state.get("current_stage", "")
    decoded = state.get("decoded_response", {})
    intent = state.get("kol_intent", "")
    
    # TODO: In production:
    # - Create ticket/notification for human review
    # - Send notification to operator via WeChat/Slack/etc.
    # - Log escalation reason and context
    # - Wait for human input before proceeding
    
    escalation_reason = f"Stage: {current_stage}, Intent: {intent}"
    
    print(f"   📋 Escalation Reason: {escalation_reason}")
    print(f"   🔔 Human operator notified")
    
    # Simulate human intervention response
    human_response = f"[Human operator response for {current_stage} stage - issue resolved]"
    
    return {
        "polished_response": human_response,
        "needs_human_review": True,
        "messages": [f"[human_escalation] Escalated to human for stage: {current_stage}"],
    }


# ============================================================================
# ADVANCE STAGE NODE (推进阶段节点)
# ============================================================================

def advance_stage(state: State) -> dict:
    """
    推进阶段节点
    Advance to the next stage in the workflow.
    Called after successful completion of current stage.
    """
    current_index = state.get("current_stage_index", 0)
    current_stage = state.get("current_stage", "")
    
    next_stage, next_index = get_next_stage(current_index)
    
    if next_stage:
        print(f"➡️ [advance_stage] Moving from '{current_stage}' to '{next_stage}'")
        return {
            "current_stage": next_stage,
            "current_stage_index": next_index,
            "stage_completed": False,
            "pending_response": None,
            "decoded_response": None,
            "kol_intent": None,
            "response_type": None,
            "messages": [f"[advance] Stage advanced: {current_stage} → {next_stage}"],
        }
    else:
        print(f"🏁 [advance_stage] All stages complete!")
        return {
            "workflow_complete": True,
            "messages": ["[advance] All stages completed - workflow finished"],
        }


def conditional_advance_stage(state: State) -> Literal["continue", "end"]:
    """
    Check if we should continue to next stage or end workflow.
    """
    workflow_complete = state.get("workflow_complete", False)
    current_index = state.get("current_stage_index", 0)
    
    # Check if workflow is complete (final stage sets this)
    if workflow_complete:
        return "end"
    
    # Check if we've gone past the last stage
    if current_index >= len(STAGE_ORDER):
        return "end"
    
    return "continue"


# ============================================================================
# LEGACY COMPATIBILITY (can be removed after full migration)
# ============================================================================

# Keep these for backwards compatibility during transition
def determination_or_decorator(state: State) -> dict:
    """Legacy node - now handled by stage_processor."""
    return stage_processor(state)

def conditional_determination_or_decorator(state: State) -> Literal["determination", "decorator"]:
    """Legacy routing - always go to decorator in new flow."""
    return "decorator"

def determination(state: State) -> dict:
    """Legacy node - intent determination now in response_check."""
    return response_check(state)

def kol_response_test(state: State) -> dict:
    """Legacy node - validation now in decoder."""
    return decoder(state)
