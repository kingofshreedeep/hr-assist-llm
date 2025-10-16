# Developer Guide

This section is for maintainers and contributors.

1. Code style: follow PEP8 for Python and modern JS conventions for frontend.
2. Tests: add unit tests for backend endpoints and integration tests for the chat flow.
3. Local debugging: run `uvicorn api:app --reload` and `streamlit run app.py`.

Notes on restructuring: if you reorganize files into `backend/` and `frontend/`, update Dockerfile paths and imports accordingly.

