#!/usr/bin/env python3
"""
Test script for Google Gen AI SDK integration
"""
import asyncio
import os
from services.gemini_service import analyze_with_gemini
async def test_gemini():
    """Test the Gemini integration"""
    print("Testing Google Gen AI SDK integration...")
    
    # Test content
    test_content = "This is absolutely shocking! You must act now before it's too late! Experts say this is true but I can't provide sources."
    
    try:
        result = await analyze_with_gemini(test_content)
        print("✅ Gemini analysis successful!")
        print(f"Trust Score: {result['trust_score']}")
        print(f"Summary: {result['result_summary']}")
        print(f"Educational Breakdown: {len(result['educational_breakdown'])} issues found")
        
        for i, issue in enumerate(result['educational_breakdown'], 1):
            print(f"  {i}. {issue['title']}: {issue['explanation']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini())