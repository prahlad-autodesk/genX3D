---
sidebar_position: 3
---

# Data Models

This document describes the data models and schemas used in the genx3D API.

## Model Object

Represents a 3D model in the system.

### Schema

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "code": "string",
  "parameters": "object",
  "file_type": "string",
  "file_size": "number",
  "created_at": "string (ISO 8601)",
  "updated_at": "string (ISO 8601)",
  "tags": ["string"],
  "visibility": "string",
  "owner_id": "string"
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the model |
| `name` | string | Human-readable name |
| `description` | string | Optional description |
| `code` | string | JavaScript code for the model |
| `parameters` | object | Key-value pairs for parametric design |
| `file_type` | string | Export format (stl, step, obj) |
| `file_size` | number | Size in bytes |
| `created_at` | string | Creation timestamp |
| `updated_at` | string | Last update timestamp |
| `tags` | array | Array of tag strings |
| `visibility` | string | public, private, or shared |
| `owner_id` | string | ID of the model owner |

### Example

```json
{
  "id": "model_123",
  "name": "Parametric Gear",
  "description": "A customizable gear with configurable teeth",
  "code": "function createGear(teeth, radius) { ... }",
  "parameters": {
    "teeth": 20,
    "radius": 30,
    "thickness": 10
  },
  "file_type": "stl",
  "file_size": 1024000,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "tags": ["gear", "parametric", "mechanical"],
  "visibility": "public",
  "owner_id": "user_456"
}
```

## Chat Message Object

Represents a message in the AI chat system.

### Schema

```json
{
  "id": "string",
  "role": "string",
  "content": "string",
  "code": "string",
  "timestamp": "string (ISO 8601)",
  "model_id": "string",
  "session_id": "string"
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique message identifier |
| `role` | string | user or assistant |
| `content` | string | Text content of the message |
| `code` | string | Generated code (assistant only) |
| `timestamp` | string | Message timestamp |
| `model_id` | string | Associated model ID |
| `session_id` | string | Chat session identifier |

### Example

```json
{
  "id": "msg_123",
  "role": "assistant",
  "content": "Here's a simple cube with 20mm sides:",
  "code": "var cube = CSG.cube({center: [0,0,0], radius: [10,10,10]});",
  "timestamp": "2024-01-15T10:30:05Z",
  "model_id": "model_123",
  "session_id": "session_789"
}
```

## File Object

Represents an uploaded or generated file.

### Schema

```json
{
  "id": "string",
  "name": "string",
  "type": "string",
  "size": "number",
  "url": "string",
  "uploaded_at": "string (ISO 8601)",
  "expires_at": "string (ISO 8601)",
  "model_id": "string"
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique file identifier |
| `name` | string | Original filename |
| `type` | string | File type (stl, step, obj, etc.) |
| `size` | number | File size in bytes |
| `url` | string | Download URL |
| `uploaded_at` | string | Upload timestamp |
| `expires_at` | string | Expiration timestamp |
| `model_id` | string | Associated model ID |

### Example

```json
{
  "id": "file_123",
  "name": "gear_assembly.stl",
  "type": "stl",
  "size": 2048000,
  "url": "/api/v1/files/file_123",
  "uploaded_at": "2024-01-15T10:30:00Z",
  "expires_at": "2024-02-15T10:30:00Z",
  "model_id": "model_123"
}
```

## User Object

Represents a user account.

### Schema

```json
{
  "id": "string",
  "email": "string",
  "username": "string",
  "created_at": "string (ISO 8601)",
  "plan": "string",
  "api_usage": "object"
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique user identifier |
| `email` | string | User's email address |
| `username` | string | Username |
| `created_at` | string | Account creation timestamp |
| `plan` | string | Subscription plan (free, pro, enterprise) |
| `api_usage` | object | API usage statistics |

### Example

```json
{
  "id": "user_456",
  "email": "user@example.com",
  "username": "designer123",
  "created_at": "2024-01-01T00:00:00Z",
  "plan": "pro",
  "api_usage": {
    "requests_this_month": 1500,
    "requests_limit": 10000,
    "models_created": 25,
    "storage_used": 1073741824
  }
}
```

## API Key Object

Represents an API key for authentication.

### Schema

```json
{
  "id": "string",
  "name": "string",
  "key_prefix": "string",
  "permissions": ["string"],
  "created_at": "string (ISO 8601)",
  "expires_at": "string (ISO 8601)",
  "last_used_at": "string (ISO 8601)"
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique key identifier |
| `name` | string | Human-readable name |
| `key_prefix` | string | First 8 characters of the key |
| `permissions` | array | Array of permission strings |
| `created_at` | string | Creation timestamp |
| `expires_at` | string | Expiration timestamp |
| `last_used_at` | string | Last usage timestamp |

### Example

```json
{
  "id": "key_123",
  "name": "Production App",
  "key_prefix": "sk-123456",
  "permissions": ["models:read", "models:write", "chat:send"],
  "created_at": "2024-01-01T00:00:00Z",
  "expires_at": "2024-12-31T23:59:59Z",
  "last_used_at": "2024-01-15T10:30:00Z"
}
```

## Error Object

Standard error response format.

### Schema

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object"
  }
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `code` | string | Error code identifier |
| `message` | string | Human-readable error message |
| `details` | object | Additional error details |

### Example

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid parameter provided",
    "details": {
      "field": "name",
      "issue": "Name is required and must be non-empty"
    }
  }
}
```

## Pagination Object

Standard pagination response format.

### Schema

```json
{
  "data": ["object"],
  "pagination": {
    "page": "number",
    "limit": "number",
    "total": "number",
    "has_more": "boolean"
  }
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `data` | array | Array of objects |
| `page` | number | Current page number |
| `limit` | number | Items per page |
| `total` | number | Total number of items |
| `has_more` | boolean | Whether more pages exist |

### Example

```json
{
  "models": [
    { "id": "model_1", "name": "Gear 1" },
    { "id": "model_2", "name": "Gear 2" }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "has_more": true
  }
}
```

## Request/Response Examples

### Create Model Request

```json
{
  "name": "My New Model",
  "description": "A parametric design",
  "code": "var cube = CSG.cube({center: [0,0,0], radius: [10,10,10]});",
  "parameters": {
    "width": 20,
    "height": 20,
    "depth": 20
  },
  "tags": ["cube", "parametric"],
  "visibility": "private"
}
```

### Chat Request

```json
{
  "message": "Create a gear with 20 teeth",
  "context": "model_123",
  "model": "gpt-4o-mini",
  "temperature": 0.7
}
```

### Export Request

```json
{
  "format": "stl",
  "resolution": "high",
  "include_metadata": true
}
```

## Data Types

### Supported File Types

- `stl` - Stereolithography format
- `step` - STEP format
- `obj` - Wavefront OBJ format
- `ply` - Stanford PLY format
- `3mf` - 3D Manufacturing Format

### Visibility Options

- `public` - Visible to everyone
- `private` - Only visible to owner
- `shared` - Visible to specific users

### Permission Types

- `models:read` - Read models
- `models:write` - Create/update models
- `models:delete` - Delete models
- `chat:send` - Send chat messages
- `files:upload` - Upload files
- `files:download` - Download files

## Next Steps

- [API Endpoints](./endpoints) - Learn about available endpoints
- [Authentication](./authentication) - Understand API security
- [Chat Integration](./chat) - Deep dive into AI chat features 