# Influencer Outreach Agent (送拍Agent框架)

A modular, loop-based LangGraph workflow for influencer/KOL collaboration outreach. Built following production patterns with proper separation of concerns.

## Project Structure

```
agent_workflow/
├── mcnagent/                          # Main package
│   ├── __init__.py
│   └── langgraph/
│       ├── __init__.py
│       ├── state.py                   # State definitions & WorkflowStage enum
│       └── nodes/
│           ├── __init__.py
│           ├── pr_nodes/              # PR/Outreach nodes
│           │   ├── __init__.py
│           │   ├── pr_nodes.py        # PR_Nodes class (stage handlers)
│           │   └── greetings.py       # Greeting message pools (10 per stage)
│           └── other_nodes/           # Utility nodes
│               ├── __init__.py
│               ├── initialization.py
│               └── nodes.py           # stage_processor, decoder, response_check, etc.
├── config/
│   ├── __init__.py
│   └── settings.py                    # Configuration management
├── graph.py                           # Graph construction (loop-based)
├── main.py                            # Entry point
├── visualize_workflow.py              # Visualization utilities
├── requirements.txt
└── README.md
```

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys
```

## Quick Start

```bash
# Run the workflow
python main.py

# Visualize the structure
python visualize_workflow.py
```

## Architecture

### Loop-Based Stage Processing

The workflow uses a **loop-based architecture** where each stage follows the same processing pattern:

```
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
```

### Workflow Stages

The workflow progresses through 9 sequential stages:

| Index | Stage | Chinese | Description |
|-------|-------|---------|-------------|
| 0 | `greet` | 打招呼 | Send greeting, request social links |
| 1 | `type` | 确认类型 | Confirm collaboration terms (单推/合集/纯佣) |
| 2 | `brief` | 发送Brief | Send campaign brief for review |
| 3 | `schedule` | 确认档期 | Confirm influencer availability |
| 4 | `product` | 选品 | Handle product selection |
| 5 | `address` | 收集地址 | Collect shipping address |
| 6 | `reminder` | 提醒收货 | Send delivery reminders |
| 7 | `script_reminder` | 脚本提醒 | Send content guidelines |
| 8 | `final` | 完成消息 | Send completion notification |

### Key Components

| Component | Description |
|-----------|-------------|
| `stage_processor` | Routes to appropriate PR_Node handler based on current stage |
| `PR_Nodes` | Class containing stage-specific handlers (greet_stage, type_stage, etc.) |
| `decorator` | Polishes outgoing messages before sending |
| `await_response` | Waits for and captures KOL response |
| `decoder` | Parses response into structured format with intent detection |
| `response_check` | Determines routing: continue, question_handler, or human_escalation |
| `advance_stage` | Moves to next stage or ends workflow |

### Greeting Message System

Each stage has a pool of **10 greeting messages** that are randomly selected to add variety to outreach:

```python
# greetings.py structure
GREET_GREETINGS = ["Greeting 1", "Greeting 2", ...]  # 10 greetings
TYPE_GREETINGS = [...]
# ... one pool per stage

def get_greeting(stage: str) -> str:
    """Returns a random greeting for the specified stage."""
```

Message format: `[Random Greeting] + [LLM-generated content]`

```python
# Usage in PR_Nodes
greeting = get_greeting("greet")
llm_content = call_llm(...)  # TODO: LLM integration
outgoing_message = f"{greeting}\n\n{llm_content}"
```

## Node Descriptions

### Processing Nodes

| Node | Chinese | Description |
|------|---------|-------------|
| `initialization` | 初始化 | Setup, fetch influencer data |
| `stage_processor` | 基本流程节点 | Execute current stage's PR_Node handler |
| `decorator` | 回复内容打磨 | Polish and enhance outgoing messages |
| `await_response` | 等待回复 | Wait for KOL response (WeChat integration point) |
| `decoder` | 解码节点 | Parse response, detect intent & sentiment |
| `response_check` | 回复检查节点 | Analyze response and determine routing |
| `advance_stage` | 推进阶段 | Move to next stage or complete workflow |

### Branching Nodes

| Node | Chinese | Description |
|------|---------|-------------|
| `question_handler` | 问题处理 | Auto-answer influencer questions from knowledge base |
| `human_escalation` | 人工介入 (博主⭐) | Escalate to human operator for complex issues |

## State Schema

```python
class State(TypedDict):
    # Influencer data
    influencer_info: Optional[InfluencerInfo]
    
    # Stage tracking (loop-based)
    current_stage: str              # Current WorkflowStage value
    current_stage_index: int        # Index in STAGE_ORDER (0-8)
    stage_completed: bool           # Whether current stage action is done
    
    # Workflow tracking
    messages: Annotated[list[str], operator.add]
    
    # Collaboration details
    collaboration_type: Optional[str]   # 单推/合集/纯佣
    price_range: Optional[str]
    product_type: Optional[str]         # 寄拍/送拍/报单
    
    # Response handling
    pending_response: Optional[str]     # Raw KOL response
    polished_response: Optional[str]    # Decorated outgoing message
    decoded_response: Optional[dict]    # Parsed response with entities
    kol_intent: Optional[str]           # accept, decline, question, negotiate, unclear
    response_type: Optional[str]        # continue, question, escalation
    
    # Flags
    has_questions: bool
    needs_human_review: bool
    workflow_complete: bool
    
    # Stage confirmations
    schedule_confirmed: bool
    address_collected: bool
    product_selected: bool
    shipping_address: Optional[str]
```

## Configuration

### Environment Variables

```bash
# .env file
ENVIRONMENT=development
DEBUG=true
OPENAI_API_KEY=sk-your-api-key
OPENAI_MODEL=gpt-4
DATABASE_URL=postgresql://user:password@localhost:5432/mcnagent
```

### Settings Class

```python
from config.settings import Settings

settings = Settings()
print(settings.openai_model)  # gpt-4
print(settings.is_production())  # False
```

## How to Extend

### 1. Add Real Greetings

Edit `mcnagent/langgraph/nodes/pr_nodes/greetings.py`:

```python
GREET_GREETINGS = [
    "您好！👋 很高兴能联系到您！",
    "Hi~ 我是来自XX品牌的对接人！",
    "您好呀！关注您很久了！",
    # ... add 10 real greetings per stage
]
```

### 2. Integrate LLM

Replace placeholder content in `PR_Nodes` methods:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

@staticmethod
def greet_stage(state: State) -> dict:
    greeting = get_greeting("greet")
    
    influencer = state.get("influencer_info", {})
    prompt = f"Generate a personalized request for social links for {influencer.get('nickname')}"
    llm_content = llm.invoke(prompt).content
    
    outgoing_message = f"{greeting}\n\n{llm_content}"
    
    return {
        "polished_response": outgoing_message,
        "stage_completed": True,
        ...
    }
```

### 3. Add a New Stage

```python
# 1. Add to WorkflowStage enum in state.py
class WorkflowStage(str, Enum):
    ...
    CUSTOM = "custom"

# 2. Add to STAGE_ORDER in state.py
STAGE_ORDER = [..., WorkflowStage.CUSTOM, ...]

# 3. Add greetings pool in greetings.py
CUSTOM_GREETINGS = ["...", ...]
GREETINGS_MAP["custom"] = CUSTOM_GREETINGS

# 4. Add handler in PR_Nodes
@staticmethod
def custom_stage(state: State) -> dict:
    greeting = get_greeting("custom")
    ...

# 5. Register in PR_Nodes.get_handler()
handlers = {
    ...
    WorkflowStage.CUSTOM.value: cls.custom_stage,
}
```

### 4. Integrate WeChat API

The `await_response` node is the integration point for messaging platforms:

```python
def await_response(state: State) -> dict:
    # Send message via WeChat
    wechat_api.send_message(
        to=state["influencer_info"]["contact_info"],
        message=state["polished_response"]
    )
    
    # Wait for response (webhook or polling)
    response = wechat_api.wait_for_reply(timeout=3600)
    
    return {
        "pending_response": response,
        ...
    }
```

## Next Steps

1. **Fill Greeting Pools** - Replace placeholders with real Chinese greetings
2. **Add LLM Integration** - Connect OpenAI/Anthropic for content generation
3. **WeChat Integration** - Connect messaging platform in `await_response`
4. **Database Setup** - Connect to influencer database
5. **Human Escalation UI** - Build operator dashboard for escalated cases
6. **Monitoring** - Add logging and observability

## License

MIT
