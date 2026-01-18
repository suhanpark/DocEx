# DocEx - Document Information Extraction

A full-stack application for extracting information from ID documents (passports, driver's licenses, green cards) using AI vision models.

## Features

- 📄 Upload ID document images (PNG, JPG, JPEG, GIF, BMP, TIFF)
- 🤖 AI-powered information extraction using Fireworks AI vision models
- ⚡ Real-time job status polling
- 🎨 Clean, responsive React frontend

## Tech Stack

| Layer    | Technology                          |
| -------- | ----------------------------------- |
| Frontend | React 19, Vite 7                    |
| Backend  | FastAPI, Python 3.11+               |
| AI       | Fireworks AI (Vision Language Model)|

## Project Structure

```
DocEx/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── models/       # Pydantic schemas
│   │   ├── routers/      # API endpoints
│   │   ├── services/     # Fireworks AI integration
│   │   └── store/        # In-memory job store
│   ├── run.py            # Entry point
│   └── pyproject.toml
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   └── services/     # API client
│   └── package.json
└── test_data/        # Sample documents for testing
```

## Quick Start (Local Development)

### Prerequisites

- Python 3.11+
- Node.js 18+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Fireworks AI API key

### 1. Clone & Setup

```bash
git clone <repository-url>
cd DocEx
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies with uv
uv sync

# Copy environment file and add your API key
cp .env.example .env
# Edit .env and set FIREWORKS_API_KEY=your_api_key_here

# Run the server
uv run python run.py
```

Backend will be available at `http://localhost:8080`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

## Configuration

Default values are configured for **local development**. Override them via `.env` files for deployment.

### Backend Environment Variables

| Variable            | Description                    | Default (Dev)       |
| ------------------- | ------------------------------ | ------------------- |
| `HOST`              | Server host                    | `127.0.0.1`         |
| `PORT`              | Server port                    | `8080`              |
| `RELOAD`            | Enable hot reload              | `true`              |
| `CORS_ORIGINS`      | Allowed origins (JSON array)   | localhost origins   |
| `FIREWORKS_API_KEY` | Fireworks AI API key           | Required            |

### Frontend Environment Variables

| Variable       | Description                           | Default (Dev) |
| -------------- | ------------------------------------- | ------------- |
| `VITE_API_URL` | Backend API URL (empty for dev proxy) | -             |

## API Endpoints

| Method | Endpoint                    | Description              |
| ------ | --------------------------- | ------------------------ |
| POST   | `/api/extract/submit`       | Submit document for extraction |
| GET    | `/api/extract/status/{id}`  | Check job status         |
| GET    | `/api/extract/jobs`         | List all jobs            |
| GET    | `/health`                   | Health check             |

## Deployment (Render)

### Backend (Web Service)

1. Create a new **Web Service** on Render
2. Connect your repository
3. Configure:
   - **Build Command:** `pip install uv && uv sync`
   - **Start Command:** `uv run python run.py`
   - **Root Directory:** `backend`
4. Add environment variables:
   ```
   HOST=0.0.0.0
   PORT=10000
   RELOAD=false
   CORS_ORIGINS=["https://your-frontend.onrender.com"]
   FIREWORKS_API_KEY=your_api_key
   ```

### Frontend (Static Site)

1. Create a new **Static Site** on Render
2. Connect your repository
3. Configure:
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
   - **Root Directory:** `frontend`
4. Add environment variable:
   ```
   VITE_API_URL=https://your-backend.onrender.com
   ```

## License

MIT
