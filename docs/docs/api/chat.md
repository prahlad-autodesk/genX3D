---
sidebar_position: 4
---

# Chat Integration

The genx3D chat API provides programmatic access to the AI assistant for 3D modeling tasks.

## Overview

The chat API allows you to:

- Send natural language requests to the AI assistant
- Receive generated CAD code and explanations
- Maintain conversation context across multiple messages
- Integrate AI assistance into your applications

## Authentication

All chat endpoints require authentication using your API key:

```http
Authorization: Bearer YOUR_API_KEY
```

## Core Endpoints

### Send Message

Send a message to the AI assistant and receive a response.

```http
POST /api/v1/chat
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "message": "Create a gear with 20 teeth and 40mm diameter",
  "context": "model_123",
  "model": "gpt-4o-mini",
  "temperature": 0.7
}
```

**Response:**
```json
{
  "id": "chat_123",
  "message": "Here's a parametric gear with 20 teeth and 40mm diameter:",
  "code": "function createGear(teeth, radius, thickness) {\n  var gear = CSG.cylinder({\n    start: [0, 0, 0],\n    end: [0, 0, thickness],\n    radius: radius\n  });\n  \n  for (var i = 0; i < teeth; i++) {\n    var angle = (i * 360) / teeth;\n    var tooth = CSG.cube({\n      center: [radius * Math.cos(angle * Math.PI / 180), \n               radius * Math.sin(angle * Math.PI / 180), thickness/2],\n      radius: [2, 2, thickness/2]\n    });\n    gear = gear.union(tooth);\n  }\n  \n  return gear;\n}\n\nvar myGear = createGear(20, 20, 10);",
  "timestamp": "2024-01-15T10:30:00Z",
  "session_id": "session_789"
}
```

### Get Chat History

Retrieve the conversation history for a session.

```http
GET /api/v1/chat/history?session_id=session_789&limit=50&offset=0
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "messages": [
    {
      "id": "msg_123",
      "role": "user",
      "content": "Create a gear with 20 teeth",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "id": "msg_124",
      "role": "assistant",
      "content": "Here's a parametric gear...",
      "code": "function createGear(teeth, radius) { ... }",
      "timestamp": "2024-01-15T10:30:05Z"
    }
  ],
  "total": 10,
  "has_more": false
}
```

### Clear Chat History

Clear the conversation history for a session.

```http
DELETE /api/v1/chat/history?session_id=session_789
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "success": true,
  "message": "Chat history cleared"
}
```

## Request Parameters

### Message Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | The text message to send |
| `context` | string | No | Associated model ID for context |
| `model` | string | No | AI model to use (default: gpt-4o-mini) |
| `temperature` | number | No | Creativity level (0.0-1.0, default: 0.7) |
| `session_id` | string | No | Session ID for conversation continuity |

### Supported AI Models

- `gpt-4o` - Most capable, higher cost
- `gpt-4o-mini` - Good balance (default)
- `anthropic/claude-3.5-sonnet` - Alternative perspective
- `local/llama-3.1-8b` - Local model (if available)

## Response Format

### Chat Response Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique response identifier |
| `message` | string | AI's text response |
| `code` | string | Generated CAD code (if applicable) |
| `timestamp` | string | Response timestamp |
| `session_id` | string | Session identifier |
| `model_used` | string | AI model that generated the response |
| `tokens_used` | number | Number of tokens consumed |

## Advanced Features

### Context-Aware Conversations

The AI assistant can reference your current model:

```json
{
  "message": "Make the gear teeth longer",
  "context": "model_123"
}
```

### Parameter Suggestions

Ask for design recommendations:

```json
{
  "message": "What's a good wall thickness for 3D printing this part?",
  "context": "model_123"
}
```

### Code Optimization

Request performance improvements:

```json
{
  "message": "How can I optimize this code for faster rendering?",
  "context": "model_123"
}
```

## Integration Examples

### Python Integration

```python
import requests
import json

class GenX3DChat:
    def __init__(self, api_key, base_url="http://localhost:8000/api/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def send_message(self, message, context=None, model="gpt-4o-mini"):
        """Send a message to the AI assistant."""
        payload = {
            "message": message,
            "model": model
        }
        if context:
            payload["context"] = context
        
        response = requests.post(
            f"{self.base_url}/chat",
            headers=self.headers,
            json=payload
        )
        return response.json()
    
    def get_history(self, session_id, limit=50):
        """Get chat history for a session."""
        params = {
            "session_id": session_id,
            "limit": limit
        }
        response = requests.get(
            f"{self.base_url}/chat/history",
            headers=self.headers,
            params=params
        )
        return response.json()

# Usage example
chat = GenX3DChat("your_api_key")
response = chat.send_message("Create a simple cube")
print(response["code"])
```

### JavaScript Integration

```javascript
class GenX3DChat {
  constructor(apiKey, baseUrl = 'http://localhost:8000/api/v1') {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
    this.headers = {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    };
  }

  async sendMessage(message, context = null, model = 'gpt-4o-mini') {
    const payload = {
      message,
      model
    };
    if (context) payload.context = context;

    const response = await fetch(`${this.baseUrl}/chat`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(payload)
    });
    return response.json();
  }

  async getHistory(sessionId, limit = 50) {
    const params = new URLSearchParams({
      session_id: sessionId,
      limit: limit.toString()
    });

    const response = await fetch(`${this.baseUrl}/chat/history?${params}`, {
      headers: this.headers
    });
    return response.json();
  }
}

// Usage example
const chat = new GenX3DChat('your_api_key');
chat.sendMessage('Create a simple cube')
  .then(response => console.log(response.code));
```

### React Hook

```javascript
import { useState, useCallback } from 'react';

function useGenX3DChat(apiKey) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = useCallback(async (message, context = null) => {
    setLoading(true);
    try {
      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message, context })
      });
      
      const data = await response.json();
      
      setMessages(prev => [...prev, {
        role: 'user',
        content: message
      }, {
        role: 'assistant',
        content: data.message,
        code: data.code
      }]);
      
      return data;
    } catch (error) {
      console.error('Chat error:', error);
    } finally {
      setLoading(false);
    }
  }, [apiKey]);

  return { messages, sendMessage, loading };
}
```

## Best Practices

### Message Structure

- **Be specific**: "Create a gear with 20 teeth" vs "Make a gear"
- **Include dimensions**: Specify sizes when relevant
- **Mention constraints**: "Must be 3D printable" or "For injection molding"

### Error Handling

```python
try:
    response = chat.send_message("Create a cube")
    if "error" in response:
        print(f"Error: {response['error']['message']}")
    else:
        print(f"Generated code: {response['code']}")
except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")
```

### Rate Limiting

Implement exponential backoff for rate limit errors:

```python
import time
import random

def send_message_with_retry(chat, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return chat.send_message(message)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Rate limited
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
                continue
            raise
    raise Exception("Max retries exceeded")
```

## Troubleshooting

### Common Issues

**"Invalid API key" error**
- Verify your API key is correct
- Check that the key hasn't expired
- Ensure proper Authorization header format

**"Rate limit exceeded" error**
- Implement exponential backoff
- Check your usage limits
- Consider upgrading your plan

**"Model not available" error**
- Check available models in your plan
- Use a different model parameter
- Contact support for model access

### Getting Help

- **Documentation**: Check this guide for common issues
- **API Status**: Check system status page
- **Support**: Contact support for account-specific issues

## Next Steps

- [API Endpoints](./endpoints) - Learn about all available endpoints
- [Authentication](./authentication) - Understand API security
- [Data Models](./models) - Reference data schemas 