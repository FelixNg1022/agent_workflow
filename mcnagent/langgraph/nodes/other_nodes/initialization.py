"""
Initialization node for workflow setup.
Updated for loop-based stage processing architecture.
"""

from mcnagent.langgraph.state import State, InfluencerInfo, WorkflowStage


def initialization(state: State) -> dict:
    """
    初始化节点
    Initialize the workflow:
    - Setup database connection
    - Prepare data structures  
    - Fetch influencer information
    - Set initial stage to GREET
    
    This is the entry point matching the Figma diagram:
    初始化，建立数据库，整理格式，准备信息包
    """
    print("\n" + "="*60)
    print("📋 [initialization] 初始化 - Setting up workflow...")
    print("   • 建立数据库 (Setup database)")
    print("   • 整理格式 (Prepare data structures)")
    print("   • 准备信息包 (Fetch influencer info)")
    print("="*60 + "\n")
    
    # TODO: Integrate with database/API to fetch real influencer info
    influencer_info: InfluencerInfo = {
        "profile_url": "",
        "nickname": "",
        "bio": "",
        "followers": 0,
        "content_type": "",
        "platform": "",
        "contact_info": None,
    }
    
    return {
        # Influencer data
        "influencer_info": influencer_info,
        
        # Stage tracking - start at first stage (GREET)
        "current_stage": WorkflowStage.GREET.value,
        "current_stage_index": 0,
        "stage_completed": False,
        
        # Reset all flags
        "has_questions": False,
        "needs_human_review": False,
        "is_confirmed": False,
        "schedule_confirmed": False,
        "address_collected": False,
        "product_selected": False,
        "kol_response_valid": False,
        "workflow_complete": False,
        
        # Clear response fields
        "pending_response": None,
        "polished_response": None,
        "decoded_response": None,
        "kol_intent": None,
        "response_type": None,
        
        # Log
        "messages": ["[init] Workflow initialized - starting at GREET stage"],
    }
