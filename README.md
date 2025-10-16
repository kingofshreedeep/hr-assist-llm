# Priyam AI — Professional Talent Scout Assistant

Priyam AI is an enterprise-friendly assistant for candidate screening and interview support.

See the full documentation generated in `docs/` (mkdocs): use `mkdocs serve` locally or view the snapshots in `assets/snapshots/`.

Quick start (Docker):

```powershell
docker-compose up -d --build
```

Open the frontend at `http://localhost:8501` and the API at `http://localhost:8000`.

Replace placeholder screenshots in `assets/images/` with real captures from your running site. For convenience the repository includes HTML snapshots under `assets/snapshots/` that were generated from a running instance:

- `assets/snapshots/remote_ui.html` — captured HTML of `GET /ui`
- `assets/snapshots/remote_streamlit_head.html` — head of the Streamlit root page

How to capture real screenshots (Windows):

1. Start the system: `docker-compose up -d --build`
2. Open `http://localhost:8000/ui` in a browser (or `http://localhost:8501` for Streamlit)
3. Use Windows Snipping Tool (Win+Shift+S) to capture the full window and save as PNG into `assets/images/`.
4. Commit the images and push to your remote repository.

