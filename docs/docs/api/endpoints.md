---
sidebar_position: 1
---

# API Endpoints

genx3D provides a comprehensive REST API for integrating 3D CAD modeling and AI capabilities into your applications.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Most endpoints require authentication. Include your API key in the request headers:

```bash
Authorization: Bearer YOUR_API_KEY
```

## Endpoints Overview

### Chat & AI
- `POST /chat` - Send messages to AI assistant
- `GET /chat/history` - Get chat history
- `DELETE /chat/history` - Clear chat history

### Models
- `GET /models` - List available models
- `POST /models` - Create new model
- `GET /models/{id}` - Get model details
- `PUT /models/{id}` - Update model
- `DELETE /models/{id}` - Delete model
- `POST /models/{id}/export` - Export model

### Files
- `POST /files/upload` - Upload file
- `GET /files/{id}` - Download file
- `DELETE /files/{id}` - Delete file

## Chat Endpoints

### Send Message

```http
POST /api/v1/chat
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "message": "Create a simple cube with 20mm sides",
  "context": "current_model_id",
  "model": "gpt-4o-mini"
}
```

**Response:**
```json
{
  "id": "chat_123",
  "message": "Here's the code for a 20mm cube:",
  "code": "var cube = CSG.cube({center: [0,0,0], radius: [10,10,10]});",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Get Chat History

```http
GET /api/v1/chat/history?limit=50&offset=0
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "messages": [
    {
      "id": "msg_123",
      "role": "user",
      "content": "Create a simple cube",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "id": "msg_124",
      "role": "assistant",
      "content": "Here's the code...",
      "code": "var cube = CSG.cube({...});",
      "timestamp": "2024-01-15T10:30:05Z"
    }
  ],
  "total": 50,
  "has_more": true
}
```

## Model Endpoints

### List Models

```http
GET /api/v1/models?page=1&limit=20
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "models": [
    {
      "id": "model_123",
      "name": "Gear Assembly",
      "description": "Parametric gear system",
      "file_type": "stl",
      "file_size": 1024000,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 25,
  "page": 1,
  "limit": 20
}
```

### Create Model

```http
POST /api/v1/models
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "name": "My New Model",
  "description": "A parametric design",
  "code": "var cube = CSG.cube({center: [0,0,0], radius: [10,10,10]});",
  "parameters": {
    "width": 20,
    "height": 20,
    "depth": 20
  }
}
```

**Response:**
```json
{
  "id": "model_124",
  "name": "My New Model",
  "description": "A parametric design",
  "code": "var cube = CSG.cube({center: [0,0,0], radius: [10,10,10]});",
  "parameters": {
    "width": 20,
    "height": 20,
    "depth": 20
  },
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Export Model

```http
POST /api/v1/models/{id}/export
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "format": "stl",
  "resolution": "high"
}
```

**Response:**
```json
{
  "file_id": "file_123",
  "download_url": "/api/v1/files/file_123",
  "format": "stl",
  "file_size": 2048000
}
```

## File Endpoints

### Upload File

```http
POST /api/v1/files/upload
Content-Type: multipart/form-data
Authorization: Bearer YOUR_API_KEY

file: [binary data]
```

**Response:**
```json
{
  "id": "file_123",
  "name": "model.stl",
  "size": 1024000,
  "type": "stl",
  "uploaded_at": "2024-01-15T10:30:00Z"
}
```

### Download File

```http
GET /api/v1/files/{id}
Authorization: Bearer YOUR_API_KEY
```

Returns the file as binary data with appropriate headers.

## Error Responses

All endpoints return consistent error responses:

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid parameter provided",
    "details": {
      "field": "name",
      "issue": "Name is required"
    }
  }
}
```

### Common Error Codes

- `UNAUTHORIZED` - Invalid or missing API key
- `FORBIDDEN` - Insufficient permissions
- `NOT_FOUND` - Resource not found
- `INVALID_REQUEST` - Invalid request parameters
- `RATE_LIMITED` - Too many requests
- `INTERNAL_ERROR` - Server error

## Rate Limiting

API requests are rate limited:
- **Free tier**: 100 requests/hour
- **Pro tier**: 1000 requests/hour
- **Enterprise**: Custom limits

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642233600
```

## SDKs and Libraries

### Python

```python
import requests

api_key = "your_api_key"
base_url = "http://localhost:8000/api/v1"

headers = {"Authorization": f"Bearer {api_key}"}

# Send chat message
response = requests.post(
    f"{base_url}/chat",
    json={"message": "Create a cube"},
    headers=headers
)
```

### JavaScript

```javascript
const apiKey = 'your_api_key';
const baseUrl = 'http://localhost:8000/api/v1';

const headers = {
  'Authorization': `Bearer ${apiKey}`,
  'Content-Type': 'application/json'
};

// Send chat message
fetch(`${baseUrl}/chat`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    message: 'Create a cube'
  })
});
```

## Next Steps

- [Authentication](./authentication) - Learn about API security
- [Models](./models) - Understand data models and schemas
- [Chat Integration](./chat) - Deep dive into AI chat features 