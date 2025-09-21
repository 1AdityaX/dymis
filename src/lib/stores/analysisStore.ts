import { writable } from 'svelte/store';

export interface EducationalBreakdown {
    title: string;
    explanation: string;
    quote: string;
}

export interface AnalysisResult {
    trust_score: number;
    result_summary: string;
    original_content: string;
    educational_breakdown: EducationalBreakdown[];
}

export interface AnalysisState {
    isLoading: boolean;
    error: string | null;
    results: AnalysisResult | null;
}

const initialState: AnalysisState = {
    isLoading: false,
    error: null,
    results: null
};

export const analysisStore = writable<AnalysisState>(initialState);

export function startAnalysis() {
    analysisStore.update(state => ({
        ...state,
        isLoading: true,
        error: null,
        results: null
    }));
}

export function setResults(results: AnalysisResult) {
    analysisStore.update(state => ({
        ...state,
        isLoading: false,
        error: null,
        results
    }));
}

export function setError(error: string | null) {
    analysisStore.update(state => ({
        ...state,
        isLoading: false,
        error,
        results: null
    }));
}

export function resetAnalysis() {
    analysisStore.set(initialState);
}
