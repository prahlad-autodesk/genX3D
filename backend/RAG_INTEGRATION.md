# RAG Integration for CAD Model Generation

This document explains the RAG (Retrieval-Augmented Generation) integration that allows the system to generate CAD models using retrieved CADQuery code.

## Overview

The RAG integration consists of three main components:

1. **RAGService**: Retrieves relevant CADQuery code from Pinecone vector database
2. **CADModelGenerator**: Executes retrieved code to generate STEP models
3. **Modified generate_node**: Uses RAG to generate models based on user queries

## How It Works

### 1. User Query Processing
When a user sends a query like "create a cuboid", the system:
- Routes the query to the `generate_node`
- Uses RAG to find similar CADQuery code in the database

### 2. RAG Retrieval
The `RAGService` class:
- Converts the user query to embeddings using SentenceTransformer
- Queries Pinecone vector database for similar code
- Returns the most relevant CADQuery code snippets

### 3. Model Generation
The `CADModelGenerator` class:
- Takes the retrieved CADQuery code
- Executes it in a safe environment
- Generates a STEP file with a unique ID
- Returns the model URL and metadata

### 4. File Serving
The generated models are:
- Stored in the `temp_models/` directory
- Served via FastAPI endpoints
- Accessible via URLs like `/temp_models/model_uuid.step`

## API Endpoints

### Generate Model
```
POST /graph_chat
{
    "message": "create a cuboid"
}
```

### Serve Generated Model
```
GET /temp_models/{filename}
```

## Configuration

### Environment Variables
- `GROQ_API_KEY`: API key for Groq LLM
- Pinecone API key is hardcoded in `RAGService` (should be moved to env vars)

### Dependencies
- `sentence-transformers`: For text embeddings
- `pinecone-client`: For vector database queries
- `cadquery`: For CAD model generation

## Testing

### Test RAG Service
```bash
cd backend
python test_rag_simple.py
```

### Test Full Integration
```bash
cd backend
python test_rag.py
```

## Example Usage

1. **Start the server**:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Send a query**:
   ```bash
   curl -X POST "http://localhost:8000/graph_chat" \
        -H "Content-Type: application/json" \
        -d '{"message": "create a cuboid"}'
   ```

3. **Response**:
   ```json
   {
     "success": true,
     "intent": "generate",
     "response": "{\"text\": \"✅ Generated CAD model based on 'create a cuboid'. Similarity score: 0.856\", \"model_url\": \"/temp_models/model_uuid.step\", \"model_type\": \"step\", \"original_prompt\": \"create a cuboid\", \"similarity_score\": 0.856}",
     "agent": "GenBot"
   }
   ```

4. **Access the model**:
   ```
   http://localhost:8000/temp_models/model_uuid.step
   ```

## File Structure

```
backend/
├── langgraph_app.py          # Main RAG integration
├── main.py                   # FastAPI server with model serving
├── test_rag.py              # Full integration tests
├── test_rag_simple.py       # Simple RAG tests
├── example_cadquery_code.py # Example CADQuery code
├── temp_models/             # Generated model storage
└── requirements.txt         # Updated dependencies
```

## Security Considerations

1. **Code Execution**: CADQuery code is executed in a controlled environment
2. **File Cleanup**: Temporary files should be cleaned up periodically
3. **API Keys**: Pinecone API key should be moved to environment variables
4. **Input Validation**: User queries should be validated and sanitized

## Future Improvements

1. **Code Validation**: Add validation for retrieved CADQuery code
2. **Error Handling**: Improve error handling for code execution
3. **File Cleanup**: Implement automatic cleanup of old temporary files
4. **Caching**: Add caching for frequently requested models
5. **Security**: Move API keys to environment variables
6. **Monitoring**: Add logging and monitoring for RAG performance 