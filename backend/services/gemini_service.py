import json
import logging
from typing import Dict
from google import genai
from core.config import settings

logger = logging.getLogger(__name__)

# Initialize Google Gen AI client
client = genai.Client(api_key=settings.google_api_key)


async def analyze_with_gemini(content: str) -> Dict:
    """
    Analyze content using Google AI Studio Gemini API
    """
    try:
        logger.info(f"Analyzing content with Gemini: {len(content)} characters")
        
        # Create the prompt for misinformation analysis
        prompt = f"""
        Analyze the following content for potential misinformation and provide a detailed assessment. 
        Focus on identifying manipulative techniques, lack of credible sources, emotional manipulation, 
        and other red flags that indicate misleading information.

        Content to analyze:
        {content}

        Please provide your analysis in the following JSON format:
        {{
            "trust_score": <integer between 0-100>,
            "result_summary": "<brief summary of the analysis>",
            "educational_breakdown": [
                {{
                    "title": "<issue title>",
                    "explanation": "<detailed explanation of the issue>",
                    "quote": "<specific quote from the content that exemplifies the issue>"
                }}
            ]
        }}

        Guidelines for analysis:
        - Trust score: 0-40 (High Risk), 41-70 (Medium Risk), 71-100 (Low Risk)
        - Look for: loaded language, emotional manipulation, lack of sources, logical fallacies, 
          unverifiable claims, scam characteristics, conspiracy theories, fake urgency
        - Provide specific quotes from the content to support your findings
        - Be educational and help users understand why content might be misleading
        - Consider cultural context for Indian users
        - Always respond with valid JSON format
        """
        
        # Call Gemini API
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt
        )
        
        # Parse the response
        response_text = response.text.strip()
        
        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            if '```json' in response_text:
                json_start = response_text.find('```json') + 7
                json_end = response_text.find('```', json_start)
                json_text = response_text[json_start:json_end].strip()
            elif '{' in response_text and '}' in response_text:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                json_text = response_text[json_start:json_end]
            else:
                # Fallback: create a basic response
                json_text = response_text
            
            result = json.loads(json_text)
            
            # Validate the response structure
            if not isinstance(result.get('trust_score'), int):
                result['trust_score'] = 50  # Default medium risk
            if not result.get('result_summary'):
                result['result_summary'] = "Analysis completed"
            if not result.get('educational_breakdown'):
                result['educational_breakdown'] = []
                
            logger.info(f"Gemini analysis completed with trust score: {result['trust_score']}")
            return result
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON from Gemini response: {e}")
            # Fallback response
            return {
                "trust_score": 50,
                "result_summary": "Analysis completed but response format was unexpected",
                "educational_breakdown": [
                    {
                        "title": "Analysis Note",
                        "explanation": "The AI analysis was completed but the response format was not as expected.",
                        "quote": "Response received from AI model"
                    }
                ]
            }
        
    except Exception as e:
        logger.error(f"Error in Gemini analysis: {str(e)}")
        # Return a fallback response instead of raising an error
        return {
            "trust_score": 50,
            "result_summary": f"Analysis failed: {str(e)}",
            "educational_breakdown": [
                {
                    "title": "Analysis Error",
                    "explanation": "The AI analysis encountered an error and could not complete properly.",
                    "quote": "Error occurred during analysis"
                }
            ]
        }