# Deployment

Recommended: use Docker Compose for local and staging deployments.

Production checklist:

- Use a managed Postgres instance or secure container
- Put the API behind a reverse proxy (NGINX) with TLS
- Rotate and protect LLM provider keys
- Add authentication and rate limiting

Simple Docker Compose deploy (example):

```powershell
docker-compose -f docker-compose.yml up -d --build
```

