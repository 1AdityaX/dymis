import { browser } from '$app/environment';
import type { AnalysisResult } from '$lib/stores/analysisStore';

// Get environment variables with fallbacks for SSR
const API_BASE_URL = browser ? import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000' : '';
const API_KEY = browser ? import.meta.env.VITE_API_KEY : '';

if (browser && (!API_BASE_URL || !API_KEY)) {
    console.warn('API configuration is incomplete. Please check your environment variables.');
}

export interface AnalysisRequest {
    content: string;
}

/**
 * Sends content to the backend for analysis
 * @param content The text content to analyze
 * @returns Promise with analysis results
 * @throws Error if the request fails or the response is invalid
 */
export async function analyzeContent(content: string): Promise<AnalysisResult> {
    if (!content?.trim()) {
        throw new Error('Content cannot be empty');
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': API_KEY,
                'Accept': 'application/json'
            },
            body: JSON.stringify({ content })
        });

        if (!response.ok) {
            let errorMessage = 'Analysis failed';
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorData.message || JSON.stringify(errorData);
            } catch (e) {
                errorMessage = `HTTP ${response.status}: ${response.statusText}`;
            }
            throw new Error(errorMessage);
        }

        const data = await response.json();
        
        // Basic validation of the response
        if (!data || typeof data !== 'object') {
            throw new Error('Invalid response format from server');
        }

        return data as AnalysisResult;
    } catch (error) {
        console.error('API Error:', error);
        if (error instanceof Error) {
            throw error; // Re-throw with original error message
        }
        throw new Error('Failed to analyze content. Please check your connection and try again.');
    }
}

/**
 * Health check to verify backend is reachable
 */
export async function checkBackendHealth(): Promise<boolean> {
    if (!browser) {
        console.log('Not in browser environment, skipping health check');
        return false;
    }
    
    try {
        console.log(`Checking backend health at: ${API_BASE_URL}/health`);
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            },
            credentials: 'include'
        });
        
        console.log('Health check response status:', response.status, response.statusText);
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Health check failed with status:', response.status, 'Response:', errorText);
            return false;
        }
        
        // Try to parse JSON if the response is JSON
        try {
            const data = await response.json();
            console.log('Health check response data:', data);
            return true;
        } catch (e) {
            // If not JSON, but status is 200, still consider it healthy
            console.log('Non-JSON response, but status is', response.status);
            return response.status === 200;
        }
    } catch (error) {
        console.error('Backend health check failed with error:', error);
        return false;
    }
}
