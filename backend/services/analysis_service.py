import logging
import re
from typing import Union
from models.analysis import AnalysisResponse, EducationalBreakdown
from services.cache_service import get_from_cache, set_to_cache
from services.scraper_service import scrape_url_content
from services.gemini_service import analyze_with_gemini

logger = logging.getLogger(__name__)


def is_url(content: str) -> bool:
    """Check if the content is a URL"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(url_pattern.match(content.strip()))


async def perform_analysis(content: str) -> AnalysisResponse:
    """
    Main analysis function that orchestrates the entire process
    """
    logger.info(f"Starting analysis for content type: {'URL' if is_url(content) else 'text'}")
    
    # Check cache first
    cache_key = content if is_url(content) else f"text_{hash(content)}"
    cached_result = await get_from_cache(cache_key)
    if cached_result:
        logger.info("Returning cached result")
        return cached_result
    
    # Extract text content
    if is_url(content):
        logger.info("Processing URL content")
        text_content = await scrape_url_content(content)
        original_content = content
    else:
        logger.info("Processing text content")
        text_content = content
        original_content = content
    
    if not text_content or len(text_content.strip()) < 10:
        raise ValueError("Content too short or empty to analyze")
    
    # Analyze with Gemini
    logger.info("Sending content to Gemini for analysis")
    gemini_result = await analyze_with_gemini(text_content)
    
    # Create response
    analysis_response = AnalysisResponse(
        trust_score=gemini_result["trust_score"],
        result_summary=gemini_result["result_summary"],
        original_content=original_content,
        educational_breakdown=[
            EducationalBreakdown(**item) for item in gemini_result["educational_breakdown"]
        ]
    )
    
    # Cache the result
    await set_to_cache(cache_key, analysis_response)
    logger.info(f"Analysis completed and cached with trust score: {analysis_response.trust_score}")
    
    return analysis_response
