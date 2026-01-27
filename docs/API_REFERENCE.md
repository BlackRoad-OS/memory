# API Reference

## 🔌 BlackRoad Memory API

Complete API reference for the BlackRoad Memory system.

## Base URL

```
http://localhost:5000/api/v1
```

## Authentication

All API requests require authentication:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:5000/api/v1/state
```

## Core Endpoints

### State Management

#### Get State

Retrieve a value from the state panel.

```http
GET /api/v1/state/{key}
```

**Parameters:**
- `key` (path) - The state key to retrieve

**Response:**
```json
{
  "key": "api.status",
  "value": "healthy",
  "version": 42,
  "updated_at": "2026-01-27T00:00:00Z"
}
```

**Example:**
```bash
curl -H "Authorization: Bearer $API_KEY" \
  http://localhost:5000/api/v1/state/api.status
```

#### Set State

Write a value to the state panel.

```http
POST /api/v1/state/{key}
Content-Type: application/json

{
  "value": "healthy",
  "ttl": 3600
}
```

**Parameters:**
- `key` (path) - The state key to set
- `value` (body) - The value to store
- `ttl` (body, optional) - Time-to-live in seconds

**Response:**
```json
{
  "key": "api.status",
  "version": 43,
  "updated_at": "2026-01-27T00:00:00Z"
}
```

**Example:**
```bash
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"value": "healthy"}' \
  http://localhost:5000/api/v1/state/api.status
```

#### Delete State

Remove a value from the state panel.

```http
DELETE /api/v1/state/{key}
```

**Parameters:**
- `key` (path) - The state key to delete

**Response:**
```json
{
  "deleted": true
}
```

#### List States

List all state keys matching a pattern.

```http
GET /api/v1/state?prefix={prefix}&limit={limit}
```

**Parameters:**
- `prefix` (query, optional) - Key prefix filter
- `limit` (query, optional) - Maximum results (default: 100)

**Response:**
```json
{
  "states": [
    {"key": "api.status", "version": 43},
    {"key": "api.requests", "version": 1024}
  ],
  "count": 2
}
```

### Locking

#### Acquire Lock

Acquire a distributed lock.

```http
POST /api/v1/locks/{lock_name}
Content-Type: application/json

{
  "timeout": 30,
  "ttl": 60
}
```

**Parameters:**
- `lock_name` (path) - Name of the lock
- `timeout` (body) - Max seconds to wait for lock
- `ttl` (body) - Lock time-to-live in seconds

**Response:**
```json
{
  "lock_id": "lock-12345",
  "acquired": true,
  "expires_at": "2026-01-27T00:01:00Z"
}
```

#### Release Lock

Release a previously acquired lock.

```http
DELETE /api/v1/locks/{lock_name}/{lock_id}
```

**Parameters:**
- `lock_name` (path) - Name of the lock
- `lock_id` (path) - Lock ID from acquire

**Response:**
```json
{
  "released": true
}
```

### Messaging

#### Send Message

Send a message to another service.

```http
POST /api/v1/messages
Content-Type: application/json

{
  "to": "service-b",
  "type": "request",
  "payload": {
    "action": "process_data"
  }
}
```

**Parameters:**
- `to` (body) - Recipient service
- `type` (body) - Message type
- `payload` (body) - Message payload

**Response:**
```json
{
  "message_id": "msg-67890",
  "sent_at": "2026-01-27T00:00:00Z"
}
```

#### Receive Messages

Retrieve messages for a service.

```http
GET /api/v1/messages?service={service}&limit={limit}
```

**Parameters:**
- `service` (query) - Service name
- `limit` (query, optional) - Max messages (default: 10)

**Response:**
```json
{
  "messages": [
    {
      "message_id": "msg-67890",
      "from": "service-a",
      "type": "request",
      "payload": {"action": "process_data"},
      "received_at": "2026-01-27T00:00:00Z"
    }
  ],
  "count": 1
}
```

### Agent Coordination

#### Register Agent

Register an AI agent with the system.

```http
POST /api/v1/agents
Content-Type: application/json

{
  "agent_name": "claude-123",
  "capabilities": ["python", "javascript"],
  "metadata": {}
}
```

**Response:**
```json
{
  "agent_id": "agent-abc",
  "registered_at": "2026-01-27T00:00:00Z"
}
```

#### Announce Task

Announce that an agent is working on a task.

```http
POST /api/v1/agents/{agent_id}/announce
Content-Type: application/json

{
  "task": "implement-auth",
  "files": ["auth.py"],
  "estimated_duration": 3600
}
```

**Response:**
```json
{
  "announced": true,
  "conflicts": []
}
```

#### Check Conflicts

Check if any other agents are working on similar tasks.

```http
GET /api/v1/agents/conflicts?task={task}
```

**Parameters:**
- `task` (query) - Task description or keywords

**Response:**
```json
{
  "conflicts": [
    {
      "agent_id": "agent-xyz",
      "task": "implement-authentication",
      "files": ["auth.py", "jwt.py"],
      "started_at": "2026-01-27T00:00:00Z"
    }
  ],
  "count": 1
}
```

### Context Management

#### Set Context

Store context for an AI agent.

```http
POST /api/v1/context/{agent_id}
Content-Type: application/json

{
  "context": {
    "conversation_history": [],
    "current_task": "implement-auth",
    "knowledge_base": {}
  }
}
```

**Response:**
```json
{
  "stored": true,
  "version": 5
}
```

#### Get Context

Retrieve context for an AI agent.

```http
GET /api/v1/context/{agent_id}
```

**Response:**
```json
{
  "agent_id": "agent-abc",
  "context": {
    "conversation_history": [],
    "current_task": "implement-auth"
  },
  "version": 5,
  "updated_at": "2026-01-27T00:00:00Z"
}
```

### Audit

#### Get Audit Log

Retrieve audit trail for operations.

```http
GET /api/v1/audit?service={service}&from={from}&to={to}
```

**Parameters:**
- `service` (query, optional) - Filter by service
- `from` (query, optional) - Start time (ISO 8601)
- `to` (query, optional) - End time (ISO 8601)

**Response:**
```json
{
  "entries": [
    {
      "timestamp": "2026-01-27T00:00:00Z",
      "service": "api-gateway",
      "operation": "set_state",
      "key": "api.status",
      "value": "healthy",
      "user": "service-account"
    }
  ],
  "count": 1
}
```

## Client Libraries

### Python Client

```python
from blackroad.memory import MemoryClient

# Initialize client
client = MemoryClient(
    url="http://localhost:5000",
    api_key="YOUR_API_KEY"
)

# State operations
client.set_state("api.status", "healthy")
status = client.get_state("api.status")

# Locking
with client.lock("my-resource"):
    # Critical section
    pass

# Messaging
client.send_message("service-b", "request", {"action": "process"})
messages = client.receive_messages("service-a")

# Agent coordination
client.register_agent("claude-123")
client.announce_task("implement-auth", ["auth.py"])
conflicts = client.check_conflicts("implement-auth")
```

### JavaScript Client

```javascript
const { MemoryClient } = require('@blackroad/memory-client');

// Initialize client
const client = new MemoryClient({
  url: 'http://localhost:5000',
  apiKey: 'YOUR_API_KEY'
});

// State operations
await client.setState('api.status', 'healthy');
const status = await client.getState('api.status');

// Locking
const lock = await client.acquireLock('my-resource');
try {
  // Critical section
} finally {
  await lock.release();
}

// Messaging
await client.sendMessage('service-b', 'request', { action: 'process' });
const messages = await client.receiveMessages('service-a');

// Agent coordination
await client.registerAgent('claude-123');
await client.announceTask('implement-auth', ['auth.py']);
const conflicts = await client.checkConflicts('implement-auth');
```

### Go Client

```go
package main

import (
    "github.com/BlackRoad-OS/memory-go-client"
)

func main() {
    // Initialize client
    client := memory.NewClient(memory.Config{
        URL:    "http://localhost:5000",
        APIKey: "YOUR_API_KEY",
    })

    // State operations
    client.SetState("api.status", "healthy")
    status, _ := client.GetState("api.status")

    // Locking
    lock, _ := client.AcquireLock("my-resource", 30)
    defer lock.Release()

    // Messaging
    client.SendMessage("service-b", "request", map[string]interface{}{
        "action": "process",
    })
    messages, _ := client.ReceiveMessages("service-a")

    // Agent coordination
    client.RegisterAgent("claude-123")
    client.AnnounceTask("implement-auth", []string{"auth.py"})
    conflicts, _ := client.CheckConflicts("implement-auth")
}
```

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

### Common Error Codes

- `INVALID_REQUEST` - Malformed request (400)
- `UNAUTHORIZED` - Invalid or missing credentials (401)
- `FORBIDDEN` - Insufficient permissions (403)
- `NOT_FOUND` - Resource not found (404)
- `CONFLICT` - Resource conflict (409)
- `RATE_LIMITED` - Too many requests (429)
- `INTERNAL_ERROR` - Server error (500)

## Rate Limits

Default rate limits per API key:

- **Read operations**: 1000 req/min
- **Write operations**: 100 req/min
- **Lock operations**: 50 req/min

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1611792000
```

## Webhooks

Subscribe to events:

```http
POST /api/v1/webhooks
Content-Type: application/json

{
  "url": "https://myservice.com/webhook",
  "events": ["state.changed", "lock.acquired"],
  "filter": {"key": "api.*"}
}
```

Event payload:
```json
{
  "event": "state.changed",
  "timestamp": "2026-01-27T00:00:00Z",
  "data": {
    "key": "api.status",
    "old_value": "degraded",
    "new_value": "healthy"
  }
}
```

---

**Built with 🖤 by BlackRoad OS**
