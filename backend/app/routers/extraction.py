import uuid
from pathlib import Path
from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from ..models.schemas import (
    JobStatus,
    SubmitResponse,
    JobStatusResponse,
    JobInfo,
)
from ..store.job_store import job_store
from ..services.task_processor import process_extraction_task
from ..config import settings


router = APIRouter(prefix="/api/extract", tags=["extraction"])


def validate_file(file: UploadFile) -> None:
    """Validate uploaded file."""
    # Check file extension
    if file.filename:
        ext = Path(file.filename).suffix.lower()
        if ext not in settings.allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type '{ext}' not allowed. Allowed types: {settings.allowed_extensions}",
            )


@router.post("/submit", response_model=SubmitResponse)
async def submit_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="ID document image to extract"),
):
    """
    Submit a document for async extraction.
    
    Returns a job ID that can be used to check the status and retrieve results.
    """
    # Validate file
    validate_file(file)
    
    # Read file content
    content = await file.read()
    
    # Check file size
    if len(content) > settings.max_file_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {settings.max_file_size // (1024*1024)}MB",
        )
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Create job in store
    await job_store.create_job(
        job_id=job_id,
        filename=file.filename or "document.jpg",
        image_data=content,
    )
    
    # Add background task for processing
    background_tasks.add_task(process_extraction_task, job_id)
    
    return SubmitResponse(
        job_id=job_id,
        status=JobStatus.PENDING,
        message="Document submitted for extraction. Use the job ID to check status.",
    )


@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """
    Check the status of an extraction job.
    
    Returns the current status and result if completed.
    """
    job = await job_store.get_job(job_id)
    
    if not job:
        raise HTTPException(
            status_code=404,
            detail=f"Job '{job_id}' not found",
        )
    
    return JobStatusResponse(
        job_id=job.job_id,
        status=job.status,
        created_at=job.created_at,
        completed_at=job.completed_at,
        result=job.result,
        error=job.error,
    )


@router.get("/jobs", response_model=List[JobStatusResponse])
async def list_jobs():
    """
    List all jobs (for debugging purposes).
    """
    jobs = await job_store.list_jobs()
    return [
        JobStatusResponse(
            job_id=job.job_id,
            status=job.status,
            created_at=job.created_at,
            completed_at=job.completed_at,
            result=job.result,
            error=job.error,
        )
        for job in jobs
    ]


@router.delete("/jobs/cleanup")
async def cleanup_jobs():
    """
    Remove expired jobs from the store.
    """
    count = await job_store.cleanup_expired_jobs()
    return {"message": f"Cleaned up {count} expired jobs"}
