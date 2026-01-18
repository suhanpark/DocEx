# DocEx Backend

FastAPI backend for the DocEx document extraction application.

## Tech Stack

- Python 3.11+
- FastAPI
- Fireworks AI (Vision Language Model)
- Pydantic
- httpx

## Setup

```bash
# Install dependencies with uv
uv sync

# Copy environment file
cp .env.example .env

# Edit .env and add your Fireworks AI API key

# Run the server
uv run python run.py
```

The server runs at `http://localhost:8080` by default.

## Configuration

All settings can be configured via environment variables in `.env`:

| Variable            | Description                    | Default                                   |
| ------------------- | ------------------------------ | ----------------------------------------- |
| `HOST`              | Server host                    | `127.0.0.1`                               |
| `PORT`              | Server port                    | `8080`                                    |
| `RELOAD`            | Enable hot reload              | `true`                                    |
| `CORS_ORIGINS`      | Allowed origins (JSON array)   | `["http://localhost:5173", ...]`          |
| `FIREWORKS_API_KEY` | Fireworks AI API key           | Required                                  |
| `FIREWORKS_MODEL`   | Model deployment path          | `accounts/simon7233/deployments/doy4esx1` |

Default values are configured for local development. Override them in `.env` for deployment.

## API Endpoints

| Method | Endpoint                    | Description                    |
| ------ | --------------------------- | ------------------------------ |
| POST   | `/api/extract/submit`       | Submit document for extraction |
| GET    | `/api/extract/status/{id}`  | Check job status               |
| GET    | `/api/extract/jobs`         | List all jobs                  |
| GET    | `/`                         | API info                       |
| GET    | `/health`                   | Health check                   |

## Project Structure

```
app/
├── models/
│   └── schemas.py            # Pydantic models
├── routers/
│   └── extraction.py         # API routes
├── services/
│   ├── fireworks_service.py  # Fireworks AI integration
│   └── task_processor.py     # Background job processing
├── store/
│   └── job_store.py          # In-memory job storage
├── config.py                 # Settings & configuration
├── cors.py                   # CORS middleware setup
└── main.py                   # FastAPI application
```

## Deployment (Render)

1. Create a new Web Service on Render
2. Set build command: `pip install uv && uv sync`
3. Set start command: `uv run python run.py`
4. Add environment variables:
   - `HOST=0.0.0.0`
   - `PORT=10000`
   - `RELOAD=false`
   - `CORS_ORIGINS=["https://your-frontend.onrender.com"]`
   - `FIREWORKS_API_KEY=your_key`

## Supported File Types

- PNG, JPG, JPEG, GIF, BMP, TIFF
- Max file size: 10MB
