import logging
from fastapi import FastAPI
from .cors import setup_cors
from .routers import extraction_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="DocEx - Document Information Extraction",
    description="Extract information from ID documents (passports, driver's licenses, green cards) using AI",
    version="1.0.0",
)

# Setup CORS
setup_cors(app)

# Include routers
app.include_router(extraction_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "DocEx API",
        "version": "1.0.0",
        "description": "Document Information Extraction API",
        "endpoints": {
            "submit": "POST /api/extract/submit",
            "status": "GET /api/extract/status/{job_id}",
            "jobs": "GET /api/extract/jobs",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
