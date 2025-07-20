---
sidebar_position: 3
---

# Configuration Guide

Learn how to configure genx3D for your specific needs and environment.

## Environment Variables

genx3D uses environment variables for configuration. Create a `.env` file in your project root:

### Required Variables

```env
# OpenRouter API Key (required for AI features)
OPENROUTER_API_KEY=your_api_key_here
```

### Optional Variables

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false

# AI Model Configuration
AI_MODEL=gpt-4o-mini
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=2000

# File Storage
UPLOAD_DIR=./static
MAX_FILE_SIZE=10485760  # 10MB in bytes

# Security
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
API_KEY_HEADER=X-API-Key
```

## Docker Configuration

### Custom Dockerfile

You can customize the Docker build by modifying the `Dockerfile`:

```dockerfile
# Use a different base image
FROM continuumio/miniconda3:latest

# Add custom packages
RUN conda install -c conda-forge additional-package

# Custom environment setup
COPY custom_environment.yml .
RUN conda env create -f custom_environment.yml
```

### Docker Compose

For more complex deployments, create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  genx3d:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - DEBUG=false
    volumes:
      - ./static:/app/static
      - ./models:/app/models
    restart: unless-stopped

  # Optional: Add a database
  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=genx3d
      - POSTGRES_USER=genx3d
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## API Configuration

### Rate Limiting

Configure rate limiting in your FastAPI app:

```python
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/chat")
@limiter.limit("10/minute")
async def chat_endpoint(request: Request):
    # Your chat logic here
    pass
```

### CORS Configuration

Configure CORS for web applications:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## AI Model Configuration

### Model Selection

Choose different AI models by setting the `AI_MODEL` environment variable:

```env
# GPT-4 (most capable, higher cost)
AI_MODEL=gpt-4o

# GPT-4o Mini (good balance)
AI_MODEL=gpt-4o-mini

# Claude (alternative)
AI_MODEL=anthropic/claude-3.5-sonnet

# Local models (if available)
AI_MODEL=local/llama-3.1-8b
```

### Temperature and Tokens

Adjust AI response characteristics:

```env
# Lower temperature = more focused responses
AI_TEMPERATURE=0.3

# Higher temperature = more creative responses
AI_TEMPERATURE=0.9

# Maximum response length
AI_MAX_TOKENS=4000
```

## File Storage Configuration

### Local Storage

Configure local file storage:

```env
# Storage directory
UPLOAD_DIR=./static

# Maximum file size (10MB)
MAX_FILE_SIZE=10485760

# Allowed file types
ALLOWED_EXTENSIONS=stl,step,obj,ply
```

### Cloud Storage

For production, consider cloud storage:

```python
# Example: AWS S3 configuration
import boto3

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)
```

## Security Configuration

### API Key Authentication

Enable API key authentication:

```env
# Enable API key header
API_KEY_HEADER=X-API-Key

# Required API key
REQUIRED_API_KEY=your-secure-api-key
```

### HTTPS Configuration

For production, configure HTTPS:

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem"
    )
```

## Monitoring and Logging

### Logging Configuration

Configure logging levels:

```env
# Log level
LOG_LEVEL=INFO

# Log file
LOG_FILE=./logs/genx3d.log

# Enable structured logging
STRUCTURED_LOGGING=true
```

### Health Checks

Add health check endpoints:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }

@app.get("/health/ai")
async def ai_health_check():
    # Test AI connection
    try:
        # Your AI health check logic
        return {"ai_status": "healthy"}
    except Exception as e:
        return {"ai_status": "unhealthy", "error": str(e)}
```

## Performance Tuning

### Database Configuration

If using a database:

```env
# Database URL
DATABASE_URL=postgresql://user:password@localhost/genx3d

# Connection pool settings
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

### Caching

Configure caching for better performance:

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="genx3d-cache")
```

## Environment-Specific Configurations

### Development

```env
DEBUG=true
LOG_LEVEL=DEBUG
AI_TEMPERATURE=0.9
```

### Production

```env
DEBUG=false
LOG_LEVEL=WARNING
AI_TEMPERATURE=0.3
CORS_ORIGINS=https://yourdomain.com
```

### Testing

```env
TESTING=true
AI_MODEL=mock
LOG_LEVEL=ERROR
```

## Next Steps

Now that you've configured genx3D, explore:

- [API Reference](../api/endpoints) - Learn about available endpoints
- [Deployment Guide](../development/deployment) - Deploy to production
- [Customization Tutorials](../tutorials/customization) - Extend functionality 