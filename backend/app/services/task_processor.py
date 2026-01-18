import asyncio
import logging
from ..store.job_store import job_store
from ..models.schemas import JobStatus
from .fireworks_service import extract_document_info

# Configure logger
logger = logging.getLogger(__name__)


async def process_extraction_task(job_id: str) -> None:
    """
    Background task to process document extraction.
    
    Args:
        job_id: The job ID to process
    """
    logger.info(f"Starting extraction task for job: {job_id}")
    
    # Small delay to ensure job is created in store
    await asyncio.sleep(0.1)
    
    # Update status to processing
    logger.info(f"Job {job_id}: Updating status to PROCESSING")
    await job_store.update_status(job_id, JobStatus.PROCESSING)
    
    try:
        # Get job info and image data
        logger.info(f"Job {job_id}: Retrieving job info")
        job = await job_store.get_job(job_id)
        if not job:
            logger.error(f"Job {job_id}: Job not found in store")
            return
        
        logger.info(f"Job {job_id}: Retrieving image data")
        image_data = await job_store.get_image_data(job_id)
        if not image_data:
            logger.error(f"Job {job_id}: Image data not found")
            await job_store.update_status(
                job_id,
                JobStatus.FAILED,
                error="Image data not found",
            )
            return
        
        logger.info(f"Job {job_id}: Image data retrieved, size: {len(image_data)} bytes")
        
        # Call Fireworks AI for extraction
        logger.info(f"Job {job_id}: Calling Fireworks AI for extraction")
        result = await extract_document_info(
            image_data=image_data,
            filename=job.filename or "document.jpg",
        )
        
        logger.info(f"Job {job_id}: Extraction completed successfully")
        
        # Update job with result
        await job_store.update_status(
            job_id,
            JobStatus.COMPLETED,
            result=result,
        )
        logger.info(f"Job {job_id}: Status updated to COMPLETED")
        
    except Exception as e:
        logger.error(f"Job {job_id}: Extraction failed with error: {type(e).__name__}: {e}")
        # Update job with error
        await job_store.update_status(
            job_id,
            JobStatus.FAILED,
            error=str(e),
        )
        logger.info(f"Job {job_id}: Status updated to FAILED")
