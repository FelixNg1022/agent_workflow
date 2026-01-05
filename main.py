"""
Main entry point for the Influencer Outreach Agent.
"""

from langgraph.checkpoint.memory import MemorySaver
from graph import build_graph
from mcnagent.langgraph.state import create_initial_state
from config.settings import Settings


def create_app():
    """
    Create the compiled workflow application with memory checkpointing.
    """
    graph = build_graph()
    
    # Add memory for conversation persistence
    memory = MemorySaver()
    
    # Compile the graph
    app = graph.compile(checkpointer=memory)
    
    return app


def run_workflow(thread_id: str = "influencer_outreach_001"):
    """
    Run the influencer outreach workflow.
    
    Args:
        thread_id: Unique identifier for this workflow instance
    """
    # Create the application
    app = create_app()
    
    # Initial state
    initial_state = create_initial_state()
    
    # Configuration with thread ID for memory
    # Increase recursion limit for loop-based workflow (9 stages × 6 nodes per stage)
    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 100,
    }
    
    print("\n" + "=" * 60)
    print("🚀 Starting Influencer Outreach Agent Workflow")
    print("=" * 60 + "\n")
    
    # Run the workflow
    for event in app.stream(initial_state, config):
        for node_name, node_state in event.items():
            print(f"\n--- Completed: {node_name} ---")
            if node_state.get("messages"):
                latest = node_state["messages"][-1] if node_state["messages"] else "N/A"
                print(f"    Latest message: {latest}")
    
    print("\n" + "=" * 60)
    print("✅ Workflow Complete")
    print("=" * 60)


def main():
    """Main function."""
    settings = Settings()
    
    if settings.debug:
        print(f"🔧 Debug mode: {settings.debug}")
        print(f"📁 Environment: {settings.environment}")
    
    run_workflow()


if __name__ == "__main__":
    main()
