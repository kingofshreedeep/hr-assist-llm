# Getting started

This section helps you get the project running locally (recommended via Docker) and includes quick checks to verify the API and frontend.

Prerequisites

- Docker & Docker Compose
- Python 3.10+ (for running scripts locally)

Quick start (Docker)

```powershell
docker-compose up -d --build
docker logs <app_container_name> --tail 200
```

Verify:

- API: http://localhost:8000/ui (serves the embedded frontend)
- Streamlit: http://localhost:8501

Environment

Create a `.env` from `.env.example` and fill in secrets. Do not commit `.env` to source control.

