# Frontend

This repository includes a standalone HTML UI (`professional_ui.html`) that can be served directly from the API (GET /ui) or embedded inside Streamlit via an iframe.

Key behaviors implemented

- Enter submits a message; Shift+Enter inserts a newline.
- The UI posts JSON payloads to the `/chat` endpoint with `user_input` and optional `session_id`.
- Theme support: the parent (Streamlit) can post a `set-theme` message to the iframe to switch light/dark.

Embedding in Streamlit

Streamlit loads the UI using an iframe and sends a postMessage to set `window.API_BASE`. See `app.py` for the integration example.
# Frontend Guide

The frontend HTML is `professional_ui.html`. It can be served directly by FastAPI at `/ui` or embedded into the Streamlit app via an iframe.

Place screenshots under `assets/images` and reference them from this page or the root `README.md`.

