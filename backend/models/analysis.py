from typing import List
from pydantic import BaseModel, Field


class EducationalBreakdown(BaseModel):
    """
    A model to hold details about a specific issue found in the content.
    """
    title: str = Field(..., description="Title of the issue found")
    explanation: str = Field(..., description="Explanation of why this is problematic")
    quote: str = Field(..., description="Direct quote from the content that exemplifies the issue")


class AnalysisRequest(BaseModel):
    """
    A model for the incoming request to analyze content.
    """
    content: str = Field(..., description="Text content or URL to analyze", min_length=1)


class AnalysisResponse(BaseModel):
    """
    A model for the structured response after analysis is complete.
    """
    trust_score: int = Field(..., description="Trust score as a percentage (0-100)", ge=0, le=100)
    result_summary: str = Field(..., description="Brief summary of the analysis result")
    original_content: str = Field(..., description="The original content that was analyzed")
    educational_breakdown: List[EducationalBreakdown] = Field(
        ..., description="A detailed breakdown of issues found in the content"
    )