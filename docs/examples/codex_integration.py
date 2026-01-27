"""
Example: Integration with BlackRoad Codex

This example demonstrates the Two-Check System:
1. Check Memory for conflicts
2. Check Codex for existing code
"""

from src.memory_client import MemoryClient
# from blackroad_codex import CodexClient  # Uncomment when available


def two_check_system(agent_name: str, task_description: str, keywords: str):
    """
    Demonstrate the Two-Check System.
    
    Args:
        agent_name: Name of the agent
        task_description: Description of the task
        keywords: Keywords for Codex search
    """
    # Initialize clients
    memory = MemoryClient(url="http://localhost:5000")
    # codex = CodexClient()  # Uncomment when available
    
    print("🔍 Two-Check System")
    print("=" * 60)
    print(f"Agent: {agent_name}")
    print(f"Task: {task_description}")
    print(f"Keywords: {keywords}\n")
    
    # Step 1: Check Memory for conflicts
    print("Step 1: [MEMORY] Checking for conflicts...")
    conflicts = memory.check_conflicts(task_description)
    
    if conflicts:
        print(f"⚠️  Conflicts detected:")
        for conflict in conflicts:
            print(f"   - Agent {conflict['agent_id']} working on: {conflict['task']}")
        print("\n❌ Cannot proceed. Coordinate with conflicting agents.\n")
        return False
    
    print("✅ No conflicts detected in Memory\n")
    
    # Step 2: Check Codex for existing code
    print("Step 2: [CODEX] Searching for existing code...")
    # existing_code = codex.search(keywords)  # Uncomment when available
    existing_code = []  # Placeholder
    
    if existing_code:
        print(f"ℹ️  Found {len(existing_code)} existing implementations:")
        for code in existing_code[:3]:  # Show first 3
            print(f"   - {code['name']} in {code['repository']}")
        print("\n💡 Reuse existing code instead of rebuilding!\n")
        return {"action": "reuse", "code": existing_code}
    
    print("✅ No existing code found in Codex\n")
    
    # Step 3: Announce work and proceed
    print("Step 3: Announcing work...")
    agent_id = memory.register_agent(agent_name, {
        "capabilities": ["coding", "analysis"],
        "version": "1.0.0"
    })
    
    result = memory.announce_task(agent_id, {
        "task": task_description,
        "status": "in-progress",
        "started_at": "2026-01-27T00:00:00Z"
    })
    
    print(f"✅ Work announced (Agent ID: {agent_id})\n")
    
    print("Summary:")
    print("-" * 60)
    print("[MEMORY] ✅ Checked for conflicts - None found")
    print("[CODEX]  ✅ Searched for existing code - None found")
    print(f"[STATUS] ✅ Proceeding with: {task_description}\n")
    
    return {"action": "implement", "task": task_description, "agent_id": agent_id}


def main():
    """Run the example."""
    print("🖤 BlackRoad Memory + Codex Integration Example\n")
    
    # Example 1: Task with no conflicts
    print("Example 1: Starting new task")
    print("=" * 60)
    result1 = two_check_system(
        agent_name="claude-123",
        task_description="implement user authentication",
        keywords="authentication jwt oauth login"
    )
    
    if result1:
        print(f"Result: {result1['action']}\n")
    
    # Example 2: Task that might conflict
    print("\nExample 2: Checking task that might conflict")
    print("=" * 60)
    
    # First, let's simulate another agent working on similar task
    memory = MemoryClient()
    agent_id_456 = memory.register_agent("claude-456", {
        "capabilities": ["coding"]
    })
    memory.announce_task(agent_id_456, {
        "task": "implement auth module",
        "status": "in-progress"
    })
    
    result2 = two_check_system(
        agent_name="claude-789",
        task_description="implement auth module",
        keywords="authentication module"
    )
    
    print("\n✅ Examples complete!")


if __name__ == "__main__":
    main()
