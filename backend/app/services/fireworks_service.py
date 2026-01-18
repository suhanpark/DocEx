import base64
import json
import logging
import re
from typing import Optional
import httpx
from ..config import settings
from ..models.schemas import ExtractionResult

# Configure logger
logger = logging.getLogger(__name__)


EXTRACTION_PROMPT = """Analyze this ID document image and extract all visible information.

You must return ONLY a valid JSON object with these fields (use null if not visible or not applicable):
{
  "document_type": "string (e.g., 'driver_license', 'passport', 'green_card', 'national_id')",
  "full_name": "string",
  "first_name": "string",
  "last_name": "string",
  "middle_name": "string",
  "date_of_birth": "string (YYYY-MM-DD format if possible)",
  "document_number": "string",
  "expiration_date": "string (YYYY-MM-DD format if possible)",
  "issue_date": "string (YYYY-MM-DD format if possible)",
  "address": "string",
  "city": "string",
  "state": "string",
  "zip_code": "string",
  "country": "string",
  "gender": "string",
  "height": "string",
  "weight": "string",
  "eye_color": "string",
  "hair_color": "string",
  "nationality": "string",
  "issuing_authority": "string",
  "class": "string (for driver's license)",
  "restrictions": "string",
  "endorsements": "string"
}

IMPORTANT: Return ONLY the JSON object, no additional text, explanation, or markdown formatting."""


def get_mime_type(filename: str) -> str:
    """Get MIME type from filename."""
    ext = filename.lower().split(".")[-1]
    mime_types = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "bmp": "image/bmp",
        "tiff": "image/tiff",
    }
    return mime_types.get(ext, "image/jpeg")


def parse_extraction_response(response_text: str) -> dict:
    """Parse the model response to extract JSON."""
    # Try to parse as-is first
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON in the response (might be wrapped in markdown code blocks)
    json_patterns = [
        r"```json\s*([\s\S]*?)\s*```",
        r"```\s*([\s\S]*?)\s*```",
        r"\{[\s\S]*\}",
    ]
    
    for pattern in json_patterns:
        match = re.search(pattern, response_text)
        if match:
            try:
                json_str = match.group(1) if "```" in pattern else match.group(0)
                return json.loads(json_str)
            except json.JSONDecodeError:
                continue
    
    # Return empty dict if parsing fails
    return {}


async def extract_document_info(
    image_data: bytes,
    filename: str,
) -> ExtractionResult:
    """
    Extract information from an ID document image using Fireworks AI.
    
    Args:
        image_data: Raw image bytes
        filename: Original filename for MIME type detection
        
    Returns:
        ExtractionResult with extracted fields
    """
    logger.info(f"Starting document extraction for file: {filename}")
    logger.info(f"Image data size: {len(image_data)} bytes")
    
    # Encode image to base64
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    mime_type = get_mime_type(filename)
    logger.info(f"Encoded image to base64, MIME type: {mime_type}")
    
    # Prepare the API request
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {settings.fireworks_api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": settings.fireworks_model,
        "max_tokens": 2048,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.1,  # Low temperature for consistent extraction
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": EXTRACTION_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{image_base64}"
                        },
                    },
                ],
            }
        ],
    }
    
    api_url = f"{settings.fireworks_base_url}/chat/completions"
    logger.info(f"Sending request to Fireworks AI: {api_url}")
    logger.info(f"Using model: {settings.fireworks_model}")
    logger.debug(f"API Key present: {bool(settings.fireworks_api_key)}")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                api_url,
                headers=headers,
                json=payload,
            )
            logger.info(f"Fireworks AI response status: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"Fireworks AI error response: {response.text}")
            
            response.raise_for_status()
            
            result = response.json()
            logger.info("Successfully received response from Fireworks AI")
            logger.debug(f"Response structure: {list(result.keys())}")
            
            raw_response = result["choices"][0]["message"]["content"]
            logger.info(f"Raw response length: {len(raw_response)} characters")
            
            # Parse the response
            extracted_fields = parse_extraction_response(raw_response)
            logger.info(f"Parsed {len(extracted_fields)} fields from response")
            
            document_type = extracted_fields.pop("document_type", None)
            logger.info(f"Document type detected: {document_type}")
            
            return ExtractionResult(
                document_type=document_type,
                fields=extracted_fields,
                raw_response=raw_response,
            )
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from Fireworks AI: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error calling Fireworks AI: {type(e).__name__}: {e}")
            raise
