# Integration Guide

## 🔗 Integrating BlackRoad Memory with the Ecosystem

This guide shows how to integrate the Memory system with other BlackRoad-OS repositories and services.

## Overview

The Memory system acts as the central coordination hub for the entire BlackRoad OS ecosystem:

```
                    ┌──────────────┐
                    │    Memory    │
                    │    System    │
                    └──────┬───────┘
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
┌─────▼─────┐      ┌──────▼──────┐      ┌─────▼─────┐
│   Codex   │      │  Scheduler  │      │   Socket  │
│  Service  │      │   Service   │      │  Service  │
└───────────┘      └─────────────┘      └───────────┘
```

## Integration with BlackRoad Codex

The [BlackRoad Codex](https://github.com/BlackRoad-OS/blackroad-os-codex) is the code intelligence system. Memory provides coordination for Codex operations.

### Setup

```python
from blackroad.memory import MemoryClient
from blackroad_codex import CodexClient

# Initialize both clients
memory = MemoryClient()
codex = CodexClient()

# Register Codex with Memory
memory.register_agent("codex-scanner")
```

### Coordination Pattern

```python
# Before indexing, check if another agent is already working
conflicts = memory.check_conflicts("indexing blackroad-os-core")

if not conflicts:
    # Announce the work
    memory.announce_task("codex-scanner", {
        "task": "indexing blackroad-os-core",
        "repo": "BlackRoad-OS/blackroad-os-core",
        "status": "in-progress"
    })
    
    # Perform the indexing
    codex.index_repository("BlackRoad-OS/blackroad-os-core")
    
    # Update status in memory
    memory.set_state("codex.index.blackroad-os-core", {
        "status": "completed",
        "components": 1379,
        "completed_at": "2026-01-27T00:00:00Z"
    })
```

### Search Integration

```python
# Store search statistics in Memory
def search_with_stats(query):
    result = codex.search(query)
    
    # Update search metrics
    memory.set_state("codex.metrics.last_search", {
        "query": query,
        "results": len(result),
        "timestamp": datetime.now().isoformat()
    })
    
    return result
```

## Integration with RoadScheduler

The [RoadScheduler](https://github.com/BlackRoad-OS/roadscheduler) manages job scheduling. Memory stores job state and coordination.

### Setup

```python
from blackroad.memory import MemoryClient
from roadscheduler import SchedulerClient

memory = MemoryClient()
scheduler = SchedulerClient()

# Register scheduler with Memory
memory.register_agent("roadscheduler")
```

### Job State Management

```python
# When scheduling a job
job_id = scheduler.schedule_job({
    "name": "backup-database",
    "schedule": "0 2 * * *",
    "action": "run_backup"
})

# Store job state in Memory
memory.set_state(f"scheduler.job.{job_id}", {
    "name": "backup-database",
    "status": "scheduled",
    "next_run": "2026-01-28T02:00:00Z"
})

# When job starts
def on_job_start(job_id):
    memory.set_state(f"scheduler.job.{job_id}.status", "running")
    memory.set_state(f"scheduler.job.{job_id}.started_at", 
                     datetime.now().isoformat())

# When job completes
def on_job_complete(job_id, result):
    memory.set_state(f"scheduler.job.{job_id}", {
        "status": "completed",
        "completed_at": datetime.now().isoformat(),
        "result": result
    })
```

### Distributed Locking for Jobs

```python
# Ensure only one instance runs a job
def run_job_safely(job_id):
    lock_name = f"job-{job_id}"
    
    with memory.lock(lock_name, timeout=300):
        # Run the job
        result = execute_job(job_id)
        
        # Update state
        memory.set_state(f"scheduler.job.{job_id}.result", result)
        
        return result
```

## Integration with RoadSocket

The [RoadSocket](https://github.com/BlackRoad-OS/roadsocket) provides network communication. Memory tracks connection state.

### Setup

```python
from blackroad.memory import MemoryClient
from roadsocket import SocketServer

memory = MemoryClient()
socket_server = SocketServer()

# Register socket service
memory.register_agent("roadsocket")
```

### Connection State Tracking

```python
# When client connects
def on_client_connect(client_id, client_info):
    memory.set_state(f"socket.connection.{client_id}", {
        "connected_at": datetime.now().isoformat(),
        "ip": client_info["ip"],
        "status": "connected"
    })

# When client disconnects
def on_client_disconnect(client_id):
    memory.set_state(f"socket.connection.{client_id}.status", "disconnected")
    memory.set_state(f"socket.connection.{client_id}.disconnected_at",
                     datetime.now().isoformat())
```

### Message Routing via Memory

```python
# Service A sends message to Service B
memory.send_message(
    to="service-b",
    type="request",
    payload={"action": "process_data", "data": "..."}
)

# Service B receives messages
messages = memory.receive_messages("service-b")
for msg in messages:
    if msg["type"] == "request":
        handle_request(msg["payload"])
```

## Integration with AI Multi-Agent System

The [BlackRoad Multi-AI System](https://github.com/BlackRoad-OS/blackroad-multi-ai-system) coordinates multiple AI agents.

### Setup

```python
from blackroad.memory import MemoryClient

memory = MemoryClient()
```

### Agent Registration

```python
# Register AI agents
agents = {
    "cecilia": "Claude",
    "cadence": "ChatGPT", 
    "silas": "Grok",
    "lucidia": "Lucidia",
    "alice": "Alice",
    "aria": "Aria"
}

for agent_name, agent_type in agents.items():
    agent_id = memory.register_agent(agent_name, {
        "type": agent_type,
        "capabilities": ["coding", "analysis", "coordination"]
    })
```

### Task Coordination

```python
# Agent announces work
def start_task(agent_name, task_description, files):
    # Check for conflicts
    conflicts = memory.check_conflicts(task_description)
    
    if conflicts:
        # Coordinate with conflicting agents
        for conflict in conflicts:
            memory.send_message(
                to=conflict["agent_id"],
                type="coordination",
                payload={
                    "from": agent_name,
                    "task": task_description,
                    "action": "coordinate"
                }
            )
        return False
    
    # No conflicts, announce the work
    memory.announce_task(agent_name, {
        "task": task_description,
        "files": files,
        "started_at": datetime.now().isoformat()
    })
    
    return True
```

### Shared Context

```python
# Store agent context
memory.set_context("cecilia", {
    "current_task": "implement authentication",
    "conversation_history": [],
    "knowledge_base": {
        "auth_patterns": ["jwt", "oauth2"],
        "libraries": ["passport", "bcrypt"]
    }
})

# Retrieve context
context = memory.get_context("cecilia")
```

## Integration with Developer Tools

### Editor Integration

For [editor-blackroadio](https://github.com/BlackRoad-OS/editor-blackroadio):

```javascript
// Track active files in memory
const memory = new MemoryClient();

editor.on('fileOpen', (filepath) => {
  memory.setState(`editor.active.${userId}`, {
    file: filepath,
    timestamp: Date.now()
  });
});

// Check if file is being edited by another user
async function checkFileConflict(filepath) {
  const allUsers = await memory.listStates('editor.active.*');
  const conflicts = allUsers.filter(u => u.value.file === filepath);
  return conflicts;
}
```

### Status Page Integration

For [blackroad-status-page](https://github.com/BlackRoad-OS/blackroad-status-page):

```javascript
// Services report health to memory
setInterval(() => {
  memory.setState('service.api.health', {
    status: 'healthy',
    uptime: process.uptime(),
    requests_per_sec: metrics.requestsPerSec
  });
}, 10000);

// Status page reads from memory
async function getSystemStatus() {
  const services = await memory.listStates('service.*.health');
  return services.map(s => ({
    name: s.key.split('.')[1],
    ...s.value
  }));
}
```

## The Two-Check System

Before any code operation in the BlackRoad ecosystem:

### 1. Check Memory

```python
# Check what other agents/services are doing
conflicts = memory.check_conflicts("authentication module")

if conflicts:
    print(f"Conflicts detected: {conflicts}")
    # Coordinate or abort
```

### 2. Check Codex

```python
# Search for existing code
from blackroad_codex import CodexClient

codex = CodexClient()
existing = codex.search("authentication jwt login")

if existing:
    print(f"Found {len(existing)} existing implementations")
    # Reuse instead of rebuild
```

### Complete Pattern

```python
def start_development(task_description, keywords):
    # Step 1: Check Memory for conflicts
    conflicts = memory.check_conflicts(task_description)
    if conflicts:
        print(f"[MEMORY] ⚠️ Conflicts detected: {conflicts}")
        return False
    
    # Step 2: Check Codex for existing code
    existing_code = codex.search(keywords)
    if existing_code:
        print(f"[CODEX] ℹ️ Found {len(existing_code)} existing implementations")
        # Reuse existing code
        return {"action": "reuse", "code": existing_code}
    
    # Step 3: Announce work and proceed
    memory.announce_task(agent_name, {
        "task": task_description,
        "status": "in-progress"
    })
    
    print("[MEMORY] ✅ Checked for conflicts")
    print("[CODEX] ✅ Searched for existing code")
    print(f"Working on: {task_description}")
    
    return {"action": "implement", "task": task_description}
```

## Best Practices

### 1. Always Register

Register your service/agent when starting:

```python
agent_id = memory.register_agent("my-service", {
    "version": "1.0.0",
    "capabilities": ["processing", "analysis"]
})
```

### 2. Use Namespaces

Organize state with clear namespaces:

```python
# Good
memory.set_state("myservice.config.db_url", "postgresql://...")
memory.set_state("myservice.metrics.requests", 1000)

# Avoid
memory.set_state("db_url", "postgresql://...")
memory.set_state("requests", 1000)
```

### 3. Clean Up

Remove state when done:

```python
try:
    # Do work
    pass
finally:
    # Clean up
    memory.delete_state("myservice.temp.data")
```

### 4. Use TTL

Set expiration for temporary data:

```python
memory.set_state("session.user.123", session_data, ttl=3600)
```

### 5. Handle Conflicts

Always check and coordinate:

```python
conflicts = memory.check_conflicts("my-task")
if conflicts:
    # Coordinate with other agents
    for conflict in conflicts:
        memory.send_message(conflict["agent_id"], "coordination", {
            "task": "my-task",
            "action": "coordinate"
        })
```

## Example: Full Integration

Complete example integrating Memory, Codex, and Scheduler:

```python
from blackroad.memory import MemoryClient
from blackroad_codex import CodexClient
from roadscheduler import SchedulerClient

# Initialize clients
memory = MemoryClient()
codex = CodexClient()
scheduler = SchedulerClient()

# Register service
agent_id = memory.register_agent("integration-service")

def process_task(task_name, keywords):
    """Complete integration example"""
    
    # 1. Check for conflicts in Memory
    conflicts = memory.check_conflicts(task_name)
    if conflicts:
        print(f"Conflicts: {conflicts}")
        return
    
    # 2. Search for existing code in Codex
    existing = codex.search(keywords)
    if existing:
        print(f"Found existing code: {existing}")
        return existing
    
    # 3. Acquire lock for exclusive access
    with memory.lock(f"task-{task_name}"):
        
        # 4. Announce work
        memory.announce_task(agent_id, {
            "task": task_name,
            "status": "in-progress"
        })
        
        # 5. Schedule periodic updates
        job_id = scheduler.schedule_job({
            "name": f"update-{task_name}",
            "interval": 60,
            "action": "update_status"
        })
        
        # 6. Do the work
        result = perform_work(task_name)
        
        # 7. Update state
        memory.set_state(f"service.{agent_id}.result", result)
        
        # 8. Index result in Codex
        codex.index_code(result)
        
        # 9. Clean up
        scheduler.cancel_job(job_id)
        memory.delete_state(f"service.{agent_id}.temp")
        
        return result

# Use it
result = process_task("implement-auth", "authentication jwt oauth")
```

---

**Built with 🖤 by BlackRoad OS**
