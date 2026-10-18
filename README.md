# SAPARTE TTM Ticket API (Demo)

Sample REST API for SAP CTS ticket validation. All records are in memory, no external ticket system or authentication. **Do not use as a production verification service.**

## Render deployment

1. Push these files to a Git repository.
2. In Render choose New > Blueprint and select the repository containing `render.yaml` (or create a Python Web Service with build command `pip install -r requirements.txt` and start command `gunicorn --bind 0.0.0.0:$PORT app:app`).
3. After deployment open `https://<your-service>.onrender.com/health`.

## API examples

- `GET /health` -> HTTP 200
- `GET /api/tickets/INC-1842` -> HTTP 200, permitted
- `GET /api/tickets/INC-2026` -> HTTP 200, permitted
- `GET /api/tickets/INC-3001` -> HTTP 200, but `sapTransportAllowed=false`
- `GET /api/tickets/INC-9999` -> HTTP 404, not found
- `GET /api/tickets/ABC` -> HTTP 400, invalid format

SAP integration should distinguish HTTP error, missing ticket and blocked ticket. HTTPS SM59 type G, SSL trust and timeout handling should be configured in SAP.
