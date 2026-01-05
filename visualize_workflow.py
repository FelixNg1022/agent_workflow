"""
Workflow Visualization Utility
Generate visual representations of the workflow graph.
Updated to reflect loop-based stage processing architecture.
"""

from graph import get_graph_visualization


def print_workflow_structure():
    """Print ASCII representation of the workflow structure."""
    
    structure = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    INFLUENCER OUTREACH AGENT WORKFLOW                        ║
║                    送拍Agent框架 (Loop-Based Architecture)                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

                                    START
                                      │
                                      ▼
                            ┌─────────────────┐
                            │  initialization │ ← 初始化：建立数据库，整理格式，准备信息包
                            └────────┬────────┘
                                     │
    ╔════════════════════════════════╧════════════════════════════════╗
    ║                   STAGE PROCESSING LOOP                         ║
    ║   Stages: greet → type → brief → schedule → product →          ║
    ║           address → reminder → script_reminder → final          ║
    ╚════════════════════════════════╤════════════════════════════════╝
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │        stage_processor         │ ← 基本流程节点
                    │   (执行当前阶段的操作)           │   Executes current stage action
                    └───────────────┬────────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      decorator      │ ← 回复内容打磨
                         │   (Polish message)  │   Enhances outgoing message
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   await_response    │ ← 等待回复
                         │  (Wait for reply)   │   Receives KOL response
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       decoder       │ ← 解码节点
                         │   (Parse response)  │   Extracts intent/entities
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   response_check    │ ← 回复检查节点
                         │  (Analyze intent)   │   Decision diamond
                         └──────────┬──────────┘
                                    │
               ┌────────────────────┼────────────────────┐
               │                    │                    │
               ▼                    ▼                    ▼
        ┌─────────────┐     ┌──────────────┐     ┌──────────────────┐
        │   continue  │     │   question   │     │    escalation    │
        │  (正常情况)  │     │  (有问题❓)  │     │    (博主 ⭐)      │
        └──────┬──────┘     └───────┬──────┘     └────────┬─────────┘
               │                    │                     │
               │                    ▼                     ▼
               │            ┌──────────────┐     ┌──────────────────┐
               │            │question_     │     │ human_escalation │
               │            │handler       │     │   (人工介入)      │
               │            └───────┬──────┘     └────────┬─────────┘
               │                    │                     │
               └────────────────────┴─────────────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   advance_stage     │ ← 推进阶段节点
                         │ (Move to next stage)│
                         └──────────┬──────────┘
                                    │
                       ┌────────────┴────────────┐
                       │                         │
                       ▼                         ▼
                 more stages              all stages done
                       │                         │
                       │                         ▼
                       │                       ┌───┐
                       │                       │END│
                       │                       └───┘
                       │
                       └──────────► (loop back to stage_processor)


═══════════════════════════════════════════════════════════════════════════════
                              STAGE DESCRIPTIONS
═══════════════════════════════════════════════════════════════════════════════

STAGES (processed in order by stage_processor):
  1. greet           - 打招呼：发送问候，获取社交平台链接
  2. type            - 合作类型：确认单推/合集/纯佣，报价，寄拍/送拍/报单
  3. brief           - 发送Brief：发送活动Brief让博主审阅
  4. schedule        - 档期确认：确认博主档期安排
  5. product         - 选品：让博主选择推广产品
  6. address         - 地址收集：收集寄送地址
  7. reminder        - 提醒收货：提醒博主确认收货
  8. script_reminder - 脚本提醒：发送内容脚本指南
  9. final           - 完成消息：发送合作完成通知

RESPONSE HANDLING NODES:
  • decorator        - 回复内容打磨：润色即将发送的消息
  • await_response   - 等待回复：接收博主回复
  • decoder          - 解码节点：解析回复内容，提取意图和实体
  • response_check   - 回复检查：分析意图并决定路由

BRANCHING HANDLERS:
  • question_handler - 问题处理：处理博主提问
  • human_escalation - 人工介入 (博主节点 ⭐)：升级至人工处理

FLOW CONTROL:
  • advance_stage    - 推进阶段：移动到下一个阶段或结束

═══════════════════════════════════════════════════════════════════════════════
                         DECISION DIAMOND LOGIC
═══════════════════════════════════════════════════════════════════════════════

After response_check, routing is based on KOL intent:

  ┌──────────────────┬─────────────────────────────────────┐
  │ Intent           │ Route                               │
  ├──────────────────┼─────────────────────────────────────┤
  │ accept           │ continue → advance_stage            │
  │ question         │ question_handler → advance_stage    │
  │ unclear          │ question_handler → advance_stage    │
  │ decline          │ human_escalation → advance_stage    │
  │ negotiate        │ human_escalation → advance_stage    │
  │ negative         │ human_escalation → advance_stage    │
  └──────────────────┴─────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
"""
    print(structure)


def generate_mermaid_diagram():
    """Generate Mermaid.js diagram for the workflow."""
    
    mermaid = """
```mermaid
flowchart TD
    START((Start)) --> init[初始化<br/>initialization]
    
    init --> stage_proc[基本流程节点<br/>stage_processor]
    
    subgraph loop[Stage Processing Loop]
        stage_proc --> decorator[回复内容打磨<br/>decorator]
        decorator --> await[等待回复<br/>await_response]
        await --> decode[解码节点<br/>decoder]
        decode --> check{回复检查<br/>response_check}
        
        check -->|正常情况| advance[推进阶段<br/>advance_stage]
        check -->|有问题| question[问题处理<br/>question_handler]
        check -->|需升级| human[人工介入 ⭐<br/>human_escalation]
        
        question --> advance
        human --> advance
    end
    
    advance -->|more stages| stage_proc
    advance -->|complete| END((End))
    
    style human fill:#ffeb3b,stroke:#f57c00
    style check fill:#e3f2fd,stroke:#1976d2
    style decorator fill:#e8f5e9,stroke:#388e3c
    style stage_proc fill:#fff3e0,stroke:#ff9800
    style loop fill:#fafafa,stroke:#9e9e9e
```
"""
    print("\nMermaid.js Diagram (paste into mermaid.live or GitHub):")
    print(mermaid)


def generate_stages_table():
    """Print a table of all stages and their functions."""
    
    table = """
═══════════════════════════════════════════════════════════════════════════════
                              STAGES TABLE
═══════════════════════════════════════════════════════════════════════════════

┌───┬─────────────────┬────────────────────────────────────────────────────────┐
│ # │ Stage           │ Description (中文)                                      │
├───┼─────────────────┼────────────────────────────────────────────────────────┤
│ 1 │ greet           │ 打招呼：发来博主介绍/发来博主去社交平台链接               │
│ 2 │ type            │ 合作类型：确认合作条件(单推/合集/纯佣)、报价、商品类型    │
│ 3 │ brief           │ 发送Brief：让博主审一下有没有问题                        │
│ 4 │ schedule        │ 档期确认：发来博主主要负按安排档期                       │
│ 5 │ product         │ 选品：让博主选品，如果无法选择到博主告诉博主              │
│ 6 │ address         │ 地址收集：发地址                                         │
│ 7 │ reminder        │ 提醒收货：产品寄送后提醒确认                             │
│ 8 │ script_reminder │ 脚本提醒：发送脚本指南和发布提醒                         │
│ 9 │ final           │ 完成消息：推全窗口加消息，完成合作                       │
└───┴─────────────────┴────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
"""
    print(table)


def save_graph_image():
    """
    Save the workflow graph as an image.
    Requires pygraphviz to be installed.
    """
    try:
        graph = get_graph_visualization()
        app = graph.compile()
        
        # Generate the graph image
        graph_png = app.get_graph().draw_mermaid_png()
        
        with open("workflow_graph.png", "wb") as f:
            f.write(graph_png)
        
        print("✅ Graph saved to workflow_graph.png")
        
    except Exception as e:
        print(f"⚠️ Could not generate graph image: {e}")
        print("   Install dependencies: pip install pygraphviz")
        print("   Or use the Mermaid diagram above.")


if __name__ == "__main__":
    print_workflow_structure()
    generate_stages_table()
    generate_mermaid_diagram()
    
    # Optionally generate image
    # save_graph_image()
