from pydantic import BaseModel
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime


class JobStatus(str, Enum):
    """Status of an extraction job."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class SubmitResponse(BaseModel):
    """Response returned when submitting a document for extraction."""
    job_id: str
    status: JobStatus
    message: str


class ExtractedField(BaseModel):
    """A single extracted field from the document."""
    field_name: str
    value: Optional[str] = None


class ExtractionResult(BaseModel):
    """Result of document extraction."""
    document_type: Optional[str] = None
    fields: Dict[str, Any] = {}
    raw_response: Optional[str] = None


class JobStatusResponse(BaseModel):
    """Response for job status check."""
    job_id: str
    status: JobStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[ExtractionResult] = None
    error: Optional[str] = None


class JobInfo(BaseModel):
    """Internal job information stored in job store."""
    job_id: str
    status: JobStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[ExtractionResult] = None
    error: Optional[str] = None
    filename: Optional[str] = None
