# Architecture

Priyam AI is designed as a small multi-service application with clear separation between API and UI.

- FastAPI serves the backend API and a convenience route (`/ui`) to host the standalone front-end HTML.
- Streamlit provides an embedded UI wrapper for alternative usage and demos.
- PostgreSQL stores conversation sessions and metadata.
- The LLM integration (Groq or local model) is managed by the backend and is called from the `/chat` endpoint.

Services:

- `app` - FastAPI + Streamlit (in the same container for simple deployments)
- `db` - PostgreSQL
