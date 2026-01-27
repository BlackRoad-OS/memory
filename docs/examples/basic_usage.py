"""
Example: Basic Memory Client Usage

This example demonstrates basic usage of the BlackRoad Memory client.
"""

from src.memory_client import MemoryClient


def main():
    # Initialize the client
    client = MemoryClient(
        url="http://localhost:5000",
        api_key="your-api-key-here"
    )
    
    print("🧠 BlackRoad Memory Client Example\n")
    
    # 1. State Management
    print("1. State Management")
    print("-" * 40)
    
    # Set state
    print("Setting state: api.status = 'healthy'")
    client.set_state("api.status", "healthy")
    
    # Get state
    status = client.get_state("api.status")
    print(f"Retrieved state: {status}\n")
    
    # 2. Distributed Locking
    print("2. Distributed Locking")
    print("-" * 40)
    
    # Using context manager
    print("Acquiring lock 'my-resource'...")
    with client.lock("my-resource", timeout=30):
        print("Lock acquired! Performing critical operation...")
        # Critical section here
        print("Operation complete!")
    print("Lock released!\n")
    
    # 3. Messaging
    print("3. Messaging")
    print("-" * 40)
    
    # Send message
    print("Sending message to 'service-b'...")
    client.send_message(
        to="service-b",
        msg_type="request",
        payload={
            "action": "process_data",
            "data": "example"
        }
    )
    print("Message sent!")
    
    # Receive messages
    print("Checking for messages...")
    messages = client.receive_messages("service-a", limit=10)
    print(f"Received {len(messages)} messages\n")
    
    # 4. Agent Coordination
    print("4. Agent Coordination")
    print("-" * 40)
    
    # Register agent
    print("Registering agent 'my-agent'...")
    agent_id = client.register_agent("my-agent", {
        "capabilities": ["python", "javascript"],
        "version": "1.0.0"
    })
    print(f"Agent registered with ID: {agent_id}")
    
    # Check for conflicts
    print("Checking for conflicts on 'implement-auth' task...")
    conflicts = client.check_conflicts("implement-auth")
    
    if not conflicts:
        print("No conflicts detected!")
        
        # Announce task
        print("Announcing task...")
        client.announce_task(agent_id, {
            "task": "implement-auth",
            "files": ["auth.py", "jwt.py"],
            "estimated_duration": 3600
        })
        print("Task announced!")
    else:
        print(f"Conflicts detected: {conflicts}")
    
    print("\n✅ Example complete!")


if __name__ == "__main__":
    main()
