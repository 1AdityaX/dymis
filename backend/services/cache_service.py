import json
import logging
import redis
from typing import Optional
from models.analysis import AnalysisResponse
from core.config import settings

logger = logging.getLogger(__name__)

# Initialize Redis connection
redis_client = redis.from_url(settings.redis_url, decode_responses=True)

# Cache TTL in seconds (24 hours)
CACHE_TTL = 24 * 60 * 60


async def get_from_cache(key: str) -> Optional[AnalysisResponse]:
    """Get analysis result from cache"""
    try:
        cached_data = redis_client.get(key)
        if cached_data:
            logger.info(f"Cache hit for key: {key}")
            data = json.loads(cached_data)
            return AnalysisResponse(**data)
        else:
            logger.info(f"Cache miss for key: {key}")
            return None
    except Exception as e:
        logger.error(f"Cache get error: {str(e)}")
        return None


async def set_to_cache(key: str, analysis_response: AnalysisResponse) -> bool:
    """Store analysis result in cache"""
    try:
        data = analysis_response.model_dump()
        redis_client.setex(key, CACHE_TTL, json.dumps(data))
        logger.info(f"Result cached with key: {key}")
        return True
    except Exception as e:
        logger.error(f"Cache set error: {str(e)}")
        return False
