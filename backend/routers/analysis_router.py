from fastapi import APIRouter, Depends, HTTPException
from models.analysis import AnalysisRequest, AnalysisResponse
from services.analysis_service import perform_analysis
from core.security import get_api_key
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    summary="Analyzes text or URL for misinformation"
)
async def analyze_content(
    request: AnalysisRequest,
    api_key: str = Depends(get_api_key)
):
    """
    Accepts a JSON body with a single `content` field, which can be
    raw text or a URL. It returns a detailed analysis.
    """
    try:
        logger.info(f"Analysis request received for content length: {len(request.content)}")
        analysis_result = await perform_analysis(content=request.content)
        logger.info(f"Analysis completed successfully with trust score: {analysis_result.trust_score}")
        return analysis_result
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Analysis failed. Please try again.",
            error_code="ANALYSIS_ERROR"
        )
