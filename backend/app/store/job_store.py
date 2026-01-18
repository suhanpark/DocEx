import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from ..models.schemas import JobStatus, JobInfo, ExtractionResult
from ..config import settings


class JobStore:
    """Thread-safe in-memory job store for tracking extraction jobs."""
    
    def __init__(self):
        self._jobs: Dict[str, JobInfo] = {}
        self._lock = asyncio.Lock()
        self._image_data: Dict[str, bytes] = {}  # Store image bytes temporarily
    
    async def create_job(self, job_id: str, filename: str, image_data: bytes) -> JobInfo:
        """Create a new job with pending status."""
        async with self._lock:
            job = JobInfo(
                job_id=job_id,
                status=JobStatus.PENDING,
                created_at=datetime.now(),
                filename=filename,
            )
            self._jobs[job_id] = job
            self._image_data[job_id] = image_data
            return job
    
    async def get_job(self, job_id: str) -> Optional[JobInfo]:
        """Get job by ID."""
        async with self._lock:
            return self._jobs.get(job_id)
    
    async def get_image_data(self, job_id: str) -> Optional[bytes]:
        """Get stored image data for a job."""
        async with self._lock:
            return self._image_data.get(job_id)
    
    async def update_status(
        self,
        job_id: str,
        status: JobStatus,
        result: Optional[ExtractionResult] = None,
        error: Optional[str] = None,
    ) -> Optional[JobInfo]:
        """Update job status and optionally set result or error."""
        async with self._lock:
            job = self._jobs.get(job_id)
            if job:
                job.status = status
                if result:
                    job.result = result
                if error:
                    job.error = error
                if status in [JobStatus.COMPLETED, JobStatus.FAILED]:
                    job.completed_at = datetime.now()
                    # Clean up image data after processing
                    self._image_data.pop(job_id, None)
            return job
    
    async def list_jobs(self) -> List[JobInfo]:
        """List all jobs."""
        async with self._lock:
            return list(self._jobs.values())
    
    async def cleanup_expired_jobs(self) -> int:
        """Remove jobs older than expiration time. Returns count of removed jobs."""
        async with self._lock:
            expiration_threshold = datetime.now() - timedelta(
                minutes=settings.job_expiration_minutes
            )
            expired_ids = [
                job_id
                for job_id, job in self._jobs.items()
                if job.created_at < expiration_threshold
            ]
            for job_id in expired_ids:
                del self._jobs[job_id]
                self._image_data.pop(job_id, None)
            return len(expired_ids)


# Global job store instance
job_store = JobStore()
