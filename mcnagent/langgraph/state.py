"""
State definitions for the influencer outreach workflow.
Updated to support loop-based stage processing matching the Figma diagram.
"""

from typing import TypedDict, Annotated, Optional, Literal
from enum import Enum
import operator


class WorkflowStage(str, Enum):
    """Enum for all workflow stages in order."""
    GREET = "greet"
    TYPE = "type"
    BRIEF = "brief"
    SCHEDULE = "schedule"
    PRODUCT = "product"
    ADDRESS = "address"
    REMINDER = "reminder"
    SCRIPT_REMINDER = "script_reminder"
    FINAL = "final"


# Ordered list of stages for sequential processing
STAGE_ORDER = [
    WorkflowStage.GREET,
    WorkflowStage.TYPE,
    WorkflowStage.BRIEF,
    WorkflowStage.SCHEDULE,
    WorkflowStage.PRODUCT,
    WorkflowStage.ADDRESS,
    WorkflowStage.REMINDER,
    WorkflowStage.SCRIPT_REMINDER,
    WorkflowStage.FINAL,
]


class InfluencerInfo(TypedDict):
    """Influencer/KOL information structure"""
    profile_url: str
    nickname: str
    bio: str
    followers: int
    content_type: str
    platform: str
    contact_info: Optional[str]


class State(TypedDict):
    """Main state for the workflow - loop-based architecture"""
    
    # Influencer data
    influencer_info: Optional[InfluencerInfo]
    
    # === Stage tracking (for loop-based processing) ===
    current_stage: str  # Current WorkflowStage value
    current_stage_index: int  # Index in STAGE_ORDER
    stage_completed: bool  # Whether current stage action is done
    
    # Workflow tracking
    messages: Annotated[list[str], operator.add]
    
    # Collaboration details
    collaboration_type: Optional[str]  # 单推/合集/纯佣
    price_range: Optional[str]
    product_type: Optional[str]  # 寄拍/送拍/报单
    
    # === Response handling (applies to each stage) ===
    pending_response: Optional[str]  # Raw KOL response waiting to be processed
    polished_response: Optional[str]  # Decorated/polished outgoing message
    decoded_response: Optional[dict]  # Parsed/decoded influencer response
    kol_intent: Optional[str]  # Determined intent: accept, decline, question, negotiate, unclear
    
    # Response routing
    response_type: Optional[str]  # "continue", "question", "escalation"
    
    # === Flags ===
    has_questions: bool
    needs_human_review: bool
    is_confirmed: bool
    
    # Stage-specific confirmations
    schedule_confirmed: bool
    address_collected: bool
    product_selected: bool
    shipping_address: Optional[str]
    
    # KOL response testing
    kol_response_valid: bool
    
    # Final state
    workflow_complete: bool


def create_initial_state() -> State:
    """Create a fresh initial state for the workflow."""
    return State(
        influencer_info=None,
        current_stage=WorkflowStage.GREET.value,
        current_stage_index=0,
        stage_completed=False,
        messages=[],
        collaboration_type=None,
        price_range=None,
        product_type=None,
        pending_response=None,
        polished_response=None,
        decoded_response=None,
        kol_intent=None,
        response_type=None,
        has_questions=False,
        needs_human_review=False,
        is_confirmed=False,
        schedule_confirmed=False,
        address_collected=False,
        product_selected=False,
        shipping_address=None,
        kol_response_valid=False,
        workflow_complete=False,
    )


def get_next_stage(current_index: int) -> tuple[Optional[str], int]:
    """
    Get the next stage in the workflow.
    Returns (next_stage_name, next_index) or (None, -1) if workflow complete.
    """
    next_index = current_index + 1
    if next_index >= len(STAGE_ORDER):
        return None, -1
    return STAGE_ORDER[next_index].value, next_index


def get_stage_by_index(index: int) -> Optional[str]:
    """Get stage name by index."""
    if 0 <= index < len(STAGE_ORDER):
        return STAGE_ORDER[index].value
    return None
