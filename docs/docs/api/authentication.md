---
sidebar_position: 2
---

# Authentication

genx3D uses API key authentication to secure access to the platform's features.

## Overview

All API requests require authentication using API keys. API keys provide access to specific features and are tied to your account.

## Getting Your API Key

### 1. Create an Account

Visit the genx3D platform and create an account:
```
https://your-genx3d-site.example.com/signup
```

### 2. Generate API Key

1. Log into your account
2. Navigate to **Settings** → **API Keys**
3. Click **Generate New Key**
4. Copy the generated key (it won't be shown again)

### 3. Store Securely

Store your API key securely:
- Never commit to version control
- Use environment variables
- Rotate keys regularly

## Using API Keys

### HTTP Headers

Include your API key in the `Authorization` header:

```http
Authorization: Bearer YOUR_API_KEY
```

### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Authorization: Bearer sk-1234567890abcdef" \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a cube"}'
```

### Python Example

```python
import requests

api_key = "sk-1234567890abcdef"
headers = {"Authorization": f"Bearer {api_key}"}

response = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={"message": "Create a cube"},
    headers=headers
)
```

### JavaScript Example

```javascript
const apiKey = 'sk-1234567890abcdef';

fetch('http://localhost:8000/api/v1/chat', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'Create a cube'
  })
});
```

## API Key Permissions

### Permission Levels

API keys can have different permission levels:

- **Read-only**: Can only read data and models
- **Standard**: Can create and modify models
- **Admin**: Full access including user management

### Scoped Access

You can create API keys with specific scopes:

```json
{
  "permissions": ["models:read", "models:write", "chat:send"],
  "rate_limit": 1000,
  "expires_at": "2024-12-31T23:59:59Z"
}
```

## Security Best Practices

### Key Management

- **Rotate regularly**: Change keys every 90 days
- **Use different keys**: Separate keys for different applications
- **Monitor usage**: Track API key usage for anomalies
- **Revoke compromised keys**: Immediately revoke if compromised

### Environment Variables

Store API keys in environment variables:

```bash
# .env file
GENX3D_API_KEY=sk-1234567890abcdef
```

```python
# Python
import os
api_key = os.getenv('GENX3D_API_KEY')
```

```javascript
// JavaScript
const apiKey = process.env.GENX3D_API_KEY;
```

### HTTPS Only

Always use HTTPS in production:
- API keys sent over HTTP are vulnerable
- genx3D enforces HTTPS for all production endpoints

## Error Responses

### Invalid API Key

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid API key",
    "details": {
      "reason": "key_not_found"
    }
  }
}
```

### Expired API Key

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "API key has expired",
    "details": {
      "expired_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### Insufficient Permissions

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Insufficient permissions",
    "details": {
      "required": "models:write",
      "provided": "models:read"
    }
  }
}
```

## Rate Limiting

API keys are subject to rate limiting:

### Rate Limit Headers

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1642233600
```

### Rate Limit Exceeded

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded",
    "details": {
      "limit": 1000,
      "reset_at": "2024-01-15T11:00:00Z"
    }
  }
}
```

## API Key Management

### List API Keys

```http
GET /api/v1/keys
Authorization: Bearer YOUR_API_KEY
```

### Create API Key

```http
POST /api/v1/keys
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "name": "My Application",
  "permissions": ["models:read", "models:write"],
  "expires_at": "2024-12-31T23:59:59Z"
}
```

### Revoke API Key

```http
DELETE /api/v1/keys/{key_id}
Authorization: Bearer YOUR_API_KEY
```

## Troubleshooting

### Common Issues

**"Invalid API key" error**
- Check that the key is correct
- Ensure the key hasn't expired
- Verify the key format (starts with `sk-`)

**"Insufficient permissions" error**
- Check your API key's permission level
- Contact support to upgrade permissions

**Rate limit errors**
- Implement exponential backoff
- Check your usage limits
- Consider upgrading your plan

### Getting Help

- **Documentation**: Check this guide for common issues
- **Support**: Contact support for account-specific issues
- **Community**: Ask questions in our community forum

## Next Steps

- [API Endpoints](./endpoints) - Learn about available endpoints
- [Models](./models) - Understand data models and schemas
- [Chat Integration](./chat) - Deep dive into AI chat features 