"""
PR_Nodes - Main flow nodes for influencer outreach workflow.
Refactored to work with loop-based stage processing architecture.
Each method handles a specific stage and generates an outgoing message.
"""

from mcnagent.langgraph.state import State, WorkflowStage
from .greetings import get_greeting


class PR_Nodes:
    """
    Public Relations node functions for influencer collaboration workflow.
    Each method represents a stage in the main outreach flow.
    Returns the outgoing message to be polished and sent.
    """
    
    # Map stage names to handler methods
    STAGE_HANDLERS = {}
    
    @classmethod
    def get_handler(cls, stage: str):
        """Get the handler method for a given stage."""
        handlers = {
            WorkflowStage.GREET.value: cls.greet_stage,
            WorkflowStage.TYPE.value: cls.type_stage,
            WorkflowStage.BRIEF.value: cls.brief_stage,
            WorkflowStage.SCHEDULE.value: cls.schedule_stage,
            WorkflowStage.PRODUCT.value: cls.product_stage,
            WorkflowStage.ADDRESS.value: cls.address_stage,
            WorkflowStage.REMINDER.value: cls.reminder_stage,
            WorkflowStage.SCRIPT_REMINDER.value: cls.script_reminder_stage,
            WorkflowStage.FINAL.value: cls.final_stage,
        }
        return handlers.get(stage)
    
    @staticmethod
    def greet_stage(state: State) -> dict:
        """
        打招呼节点
        1) Send greeting to influencer
        2) Request social platform links
        """
        print("👋 [greet_stage] Sending greeting message...")
        
        greeting = get_greeting("greet")
        # TODO: Replace with LLM-generated content
        llm_content = "我们对您的内容非常感兴趣，想与您洽谈合作事宜。请问方便分享您的社交平台链接吗？"
        outgoing_message = f"{greeting}\n\n{llm_content}"
        
        return {
            "pending_response": None,  # Clear for new response
            "polished_response": outgoing_message,
            "stage_completed": True,
            "messages": ["[greet] Greeting sent, awaiting platform links"],
        }
    
    @staticmethod
    def type_stage(state: State) -> dict:
        """
        合作类型确认节点
        Verify influencer accepts collaboration conditions:
        1) Collaboration type: 单推/合集 (solo/collection) or 纯佣 (pure commission)
        2) Price range
        3) Product type: 寄拍/送拍/报单 (send product/gift product/order-based)
        """
        print("📝 [type_stage] Confirming collaboration terms...")
        
        greeting = get_greeting("type")
        # TODO: Replace with LLM-generated content
        llm_content = "请确认以下合作条件：\n1. 合作类型：单推/合集/纯佣\n2. 报价范围\n3. 商品类型：寄拍/送拍/报单"
        outgoing_message = f"{greeting}\n\n{llm_content}"
        
        return {
            "pending_response": None,
            "polished_response": outgoing_message,
            "stage_completed": True,
            "messages": ["[type] Collaboration terms sent for confirmation"],
        }
    
    @staticmethod
    def brief_stage(state: State) -> dict:
        """
        发送Brief节点
        Send campaign brief for influencer to review.
        Check if influencer has any questions about the brief.
        """
        print("📄 [brief_stage] Sending campaign brief...")
        
        greeting = get_greeting("brief")
        # TODO: Replace with LLM-generated content
        llm_content = "请查阅附件中的活动Brief，如有任何问题请随时提出。确认无误后我们将继续下一步。"
        outgoing_message = f"{greeting}\n\n{llm_content}"
        
        return {
            "pending_response": None,
            "polished_response": outgoing_message,
            "collaboration_type": state.get("collaboration_type"),  # Preserve from type stage
            "stage_completed": True,
            "messages": ["[brief] Campaign brief sent, awaiting review"],
        }
    
    @staticmethod
    def schedule_stage(state: State) -> dict:
        """
        档期确认节点
        Confirm influencer's availability and schedule for the collaboration.
        """
        print("📅 [schedule_stage] Confirming availability...")
        
        greeting = get_greeting("schedule")
        # TODO: Replace with LLM-generated content
        llm_content = "请问您方便的档期是什么时候？我们会根据您的时间安排进行对接。"
        outgoing_message = f"{greeting}\n\n{llm_content}"
        
        return {
            "pending_response": None,
            "polished_response": outgoing_message,
            "stage_completed": True,
            "messages": ["[schedule] Schedule request sent"],
        }
    
    @staticmethod
    def product_stage(state: State) -> dict:
        """
        选品节点
        Let influencer select products. If unable to select, notify influencer directly.
        """
        print("🛍️ [product_stage] Processing product selection...")
        
        greeting = get_greeting("product")
        # TODO: Replace with LLM-generated content
        llm_content = "请从以下产品中选择您想要推广的商品，如有疑问请告知。"
        outgoing_message = f"{greeting}\n\n{llm_content}"
        
        return {
            "pending_response": None,
            "polished_response": outgoing_message,
            "schedule_confirmed": True,  # Previous stage confirmed
            "stage_completed": True,
            "messages": ["[product] Product selection options sent"],
        }
    
    @staticmethod
    def address_stage(state: State) -> dict:
        """
        地址收集节点
        Collect shipping address with product tracking link.
        """
        print("📍 [address_stage] Collecting shipping address...")
        
        greeting = get_greeting("address")
        # TODO: Replace with LLM-generated content
        llm_content = "请提供您的收货地址，我们会尽快安排产品寄送并提供物流跟踪信息。"
        outgoing_message = f"{greeting}\n\n{llm_content}"
        
        return {
            "pending_response": None,
            "polished_response": outgoing_message,
            "product_selected": True,  # Previous stage confirmed
            "stage_completed": True,
            "messages": ["[address] Address request sent"],
        }
    
    @staticmethod
    def reminder_stage(state: State) -> dict:
        """
        提醒节点
        Send reminder for package receipt confirmation.
        """
        print("🔔 [reminder_stage] Sending receipt reminder...")
        
        greeting = get_greeting("reminder")
        # TODO: Replace with LLM-generated content
        llm_content = "产品已寄出，请注意查收。收到后请确认，我们会继续对接后续事宜。"
        outgoing_message = f"{greeting}\n\n{llm_content}"
        
        return {
            "pending_response": None,
            "polished_response": outgoing_message,
            "address_collected": True,  # Previous stage confirmed
            "stage_completed": True,
            "messages": ["[reminder] Receipt reminder sent"],
        }
    
    @staticmethod
    def script_reminder_stage(state: State) -> dict:
        """
        脚本提醒节点
        Send script/content reminder to influencer.
        """
        print("📝 [script_reminder_stage] Sending content script reminder...")
        
        greeting = get_greeting("script_reminder")
        # TODO: Replace with LLM-generated content
        llm_content = "请按照Brief中的脚本指南进行内容创作，如有需要修改的地方请与我们沟通。发布时间请按照约定档期。"
        outgoing_message = f"{greeting}\n\n{llm_content}"
        
        return {
            "pending_response": None,
            "polished_response": outgoing_message,
            "stage_completed": True,
            "messages": ["[script_reminder] Script reminder sent"],
        }
    
    @staticmethod
    def final_stage(state: State) -> dict:
        """
        推全窗口加消息节点
        Send final confirmation message, complete workflow.
        """
        print("✅ [final_stage] Sending completion message...")
        
        greeting = get_greeting("final")
        # TODO: Replace with LLM-generated content
        llm_content = "感谢您的合作！如有后续合作机会，我们会再次联系您。祝一切顺利！"
        outgoing_message = f"{greeting}\n\n{llm_content}"
        
        return {
            "pending_response": None,
            "polished_response": outgoing_message,
            "stage_completed": True,
            "workflow_complete": True,
            "messages": ["[final] Workflow completed successfully"],
        }
