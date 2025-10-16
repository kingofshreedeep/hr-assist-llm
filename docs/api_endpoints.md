# API Endpoints

Detailed list of API endpoints and quick testing examples.

GET /

- Purpose: Health check & basic info
- Response: status + version info

GET /ui

- Purpose: Serve the standalone UI HTML page used for development and same-origin testing

POST /chat

- Purpose: Accepts user_input and returns an LLM-generated response
- Example usage with curl:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"user_input":"Hello","session_id":"local-1"}' \
  http://localhost:8000/chat
```

