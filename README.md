# Influencer Outreach Agent (送拍Agent框架)

A modular, tree-structured LangGraph workflow for influencer/KOL collaboration outreach. Built following production patterns with proper separation of concerns.

## Project Structure

```
agent_workflow/
├── mcnagent/                          # Main package
│   ├── __init__.py
│   └── langgraph/
│       ├── __init__.py
│       ├── state.py                   # State definitions
│       └── nodes/
│           ├── __init__.py
│           ├── pr_nodes/              # PR/Outreach nodes
│           │   ├── __init__.py
│           │   └── pr_nodes.py        # PR_Nodes class
│           └── other_nodes/           # Utility nodes
│               ├── __init__.py
│               ├── initialization.py
│               └── nodes.py           # decoder, kol_response_test, etc.
├── config/
│   ├── __init__.py
│   └── settings.py                    # Configuration management
├── graph.py                           # Graph construction
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

### Key Components

| Component | Description |
|-----------|-------------|
| `PR_Nodes` | Class-based node organization for main outreach flow |
| `State` | TypedDict-based state management with helper functions |
| `decoder` | Parses and structures influencer responses |
| `kol_response_test` | Validates KOL/influencer response quality |
| `determination` | Classifies response intent (accept/decline/question) |
| `decorator` | Polishes and enhances AI-generated responses |

### Workflow Flow

```
START
  │
  ▼
initialization ──► email_greet_run ──► determination_or_decorator
                                              │
                               ┌──────────────┴──────────────┐
                               ▼                             ▼
                        determination ──────────────► decorator
                                                          │
                                                          ▼
                                                  kol_response_test
                                                          │
                    ┌─────────────────────────────────────┘
                    ▼
             type_run ──► brief_run ──► decoder ──► determination
                                                          │
                    ┌─────────────────┬───────────────────┤
                    ▼                 ▼                   ▼
             schedule_run    question_handler    human_escalation
                    │                 │                   │
                    └─────────────────┴───────────────────┘
                                      │
             schedule_run ──► product_run ──► address_run ──► reminder_run
                                                                    │
                                                                    ▼
                                              script_reminder_run ──► final_message_run
                                                                              │
                                                                              ▼
                                                                             END
```

## Node Descriptions

### Initialization
| Node | Chinese | Description |
|------|---------|-------------|
| `initialization` | 初始化 | Setup database, fetch influencer data |

### PR_Nodes (Main Flow)
| Node | Chinese | Description |
|------|---------|-------------|
| `email_greet_run` | 打招呼 | Send greeting, request social links |
| `type_run` | 确认类型 | Confirm collaboration terms |
| `brief_run` | 发送Brief | Send campaign brief |
| `schedule_run` | 确认档期 | Confirm availability |
| `product_run` | 选品 | Handle product selection |
| `address_run` | 收集地址 | Collect shipping address |
| `reminder_run` | 提醒收货 | Send delivery reminders |
| `script_reminder_run` | 脚本提醒 | Send content guidelines |
| `final_message_run` | 完成消息 | Send completion notification |

### Response Handling
| Node | Chinese | Description |
|------|---------|-------------|
| `decoder` | 解码器 | Parse response into structured format |
| `kol_response_test` | KOL回复测试 | Validate response quality |
| `determination` | 判断 | Classify response intent |
| `decorator` | 装饰器 | Polish AI responses |
| `question_handler` | 问题处理 | Handle influencer questions |
| `human_escalation` | 人工介入 | Escalate to human operator |

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

### 1. Add LLM to a Node

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

class PR_Nodes:
    @staticmethod
    def email_greet_run(state: State) -> State:
        influencer = state.get("influencer_info", {})
        
        prompt = f"Generate a greeting for {influencer.get('nickname')}"
        response = llm.invoke(prompt)
        
        return {
            **state,
            "pending_response": response.content,
            "messages": ["Greeting generated"],
        }
```

### 2. Add a New Node

```python
# 1. Add to mcnagent/langgraph/nodes/pr_nodes/pr_nodes.py
class PR_Nodes:
    @staticmethod
    def custom_run(state: State) -> State:
        # Your logic here
        return {**state, "custom_field": "value"}

# 2. Register in graph.py
graph_builder.add_node("custom_run", PR_Nodes.custom_run)
graph_builder.add_edge("previous_node", "custom_run")
```

### 3. Add Conditional Branching

```python
def route_custom(state: State) -> Literal["option_a", "option_b"]:
    if state.get("some_condition"):
        return "option_a"
    return "option_b"

graph_builder.add_conditional_edges(
    "source_node",
    route_custom,
    {"option_a": "node_a", "option_b": "node_b"}
)
```

## State Schema

```python
class State(TypedDict):
    # Influencer data
    influencer_info: Optional[InfluencerInfo]
    
    # Workflow tracking
    current_stage: str
    messages: list[str]
    
    # Collaboration details
    collaboration_type: Optional[str]
    price_range: Optional[str]
    product_type: Optional[str]
    
    # Response handling
    pending_response: Optional[str]
    polished_response: Optional[str]
    decoded_response: Optional[dict]
    
    # KOL testing
    kol_response_valid: bool
    kol_intent: Optional[str]
    
    # Flow control
    has_questions: bool
    needs_human_review: bool
    workflow_complete: bool
```

## Next Steps

1. **Add LLM Integration** - Connect OpenAI/Anthropic for response generation
2. **Database Setup** - Connect to influencer database
3. **Message Queue** - Integrate with WeChat/messaging platforms
4. **Web Backend** - Add API endpoints (see reference: `server.py`)
5. **Monitoring** - Add logging and observability

## License

MIT
