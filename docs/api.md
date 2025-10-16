# API Overview

This project exposes a small set of JSON endpoints used by the web UI and integrations.

Main endpoints

- GET / -> Health & service info
- GET /ui -> Serves the standalone HTML frontend (`professional_ui.html`)
- POST /chat -> Chat endpoint

POST /chat

Request (JSON):

```json
{
  "user_input": "Hello, summarize this candidate",
  "session_id": "optional-session-id"
}
```

Response (JSON):

```json
{
  "session_id": "generated-session-id",
  "response": "AI-generated text",
  "metadata": { }
}
```

Security notes

- Ensure the `GROQ_API_KEY` and other secrets are set in environment variables and not committed.
- Rotate any exposed keys immediately.
# API Reference

This document will describe the backend API endpoints. Add examples and screenshots under `assets/images`.

- GET / -> Basic info
- POST /chat -> Chat endpoint: Accepts JSON { session_id?: string, user_input: string }
- GET /sessions/{session_id} -> Retrieve session history
- GET /ui -> Serves the HTML UI
