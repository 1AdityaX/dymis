<script lang="ts">
	import { onMount } from 'svelte';
	import Button from '$lib/components/ui/button.svelte';
	import Textarea from '$lib/components/ui/textarea.svelte';
	import Card from '$lib/components/ui/card.svelte';
	import CardContent from '$lib/components/ui/card-content.svelte';
	import ResultsView from '$lib/components/ResultsView.svelte';
	import { analysisStore, startAnalysis, setResults, setError, resetAnalysis } from '$lib/stores/analysisStore';
	import { analyzeContent, checkBackendHealth } from '$lib/api';
	import { Loader, AlertCircle, CheckCircle2 } from 'lucide-svelte';

	let content = $state('');
	let isBackendAvailable = $state<boolean | null>(null);
	let isCheckingBackend = $state(false);
	let { isLoading, error, results } = $derived($analysisStore);

	// Check backend health on component mount
	onMount(() => {
		console.log('Component mounted, checking backend health...');
		// Use an immediately-invoked async function expression (IIFE)
		let isMounted = true;
		
		const checkHealth = async () => {
			if (!isMounted) return;
			
			isCheckingBackend = true;
			try {
				console.log('Calling checkBackendHealth()...');
				const isAvailable = await checkBackendHealth();
				console.log('Backend available:', isAvailable);
				
				if (isMounted) {
					isBackendAvailable = isAvailable;
					if (!isAvailable) {
						console.log('Backend is not available, showing error');
						setError('Backend service is unavailable. Please try again later.');
					} else {
						// Clear any previous errors if backend is now available
						setError(null);
					}
				}
			} catch (err) {
				console.error('Error checking backend health:', err);
				if (isMounted) {
					isBackendAvailable = false;
					setError('Failed to connect to the analysis service. Please check your connection and ensure the backend is running.');
				}
			} finally {
				if (isMounted) {
					isCheckingBackend = false;
					console.log('Backend check completed. isBackendAvailable:', isBackendAvailable, 'isCheckingBackend:', isCheckingBackend);
				}
			}
		};
		
		// Initial check
		checkHealth();
		
		// Set up periodic health check (every 30 seconds)
		const healthCheckInterval = setInterval(checkHealth, 30000);

		// Cleanup function
		return () => {
			isMounted = false;
			clearInterval(healthCheckInterval);
		};
	});

	// Debug log when states change
	$effect(() => {
		console.log('State update - isBackendAvailable:', isBackendAvailable, 
			'isCheckingBackend:', isCheckingBackend, 
			'isLoading:', isLoading, 
			'content length:', content.trim().length);
	});

	async function handleAnalyze() {
		if (!content.trim() || !isBackendAvailable) return;

		startAnalysis();

		try {
			const analysisResults = await analyzeContent(content);
			setResults(analysisResults);
		} catch (err) {
			console.error('Analysis error:', err);
			const errorMessage = err instanceof Error ? err.message : 'Failed to analyze content. Please try again.';
			setError(errorMessage);
		}
	}

	function resetForm() {
		content = '';
		resetAnalysis();
	}
</script>

<div class="space-y-8">
	<!-- Header -->
	<div class="space-y-4 text-center">
		<h1 class="text-4xl font-bold text-slate-800">Dymis</h1>
		<p class="text-lg text-slate-600">Analyze with clarity. Fight misinformation.</p>
	</div>

	{#if results}
		<!-- Results View -->
		<ResultsView {results} />
	{:else}
		<!-- Input View -->
		<Card>
			<CardContent class="p-6">
				<div class="space-y-4">
					<label for="content-input" class="block text-sm font-medium text-slate-700">
						Paste text or a website URL to analyze...
					</label>
					<Textarea
						id="content-input"
						bind:value={content}
						placeholder="Paste text or a website URL to analyze..."
						class="min-h-32"
						on:input={() => console.log('Content changed:', content, 'Trimmed length:', content.trim().length)}
						disabled={isLoading}
					/>

					{#if isCheckingBackend}
						<div class="rounded-md border border-blue-200 bg-blue-50 p-3 flex items-start">
							<Loader class="h-5 w-5 text-blue-500 mr-2 mt-0.5 animate-spin" />
							<p class="text-sm text-blue-700">Checking backend connection...</p>
						</div>
					{:else if !isBackendAvailable}
						<div class="rounded-md border border-red-200 bg-red-50 p-3 flex items-start">
							<AlertCircle class="h-5 w-5 text-red-500 mr-2 mt-0.5" />
							<div>
								<p class="text-sm font-medium text-red-800">Backend Service Unavailable</p>
								<p class="text-sm text-red-700 mt-1">
									The analysis service is currently unavailable. Please try again later.
								</p>
							</div>
						</div>
					{:else if error}
						<div class="rounded-md border border-red-200 bg-red-50 p-3 flex items-start">
							<AlertCircle class="h-5 w-5 text-red-500 mr-2 mt-0.5" />
							<div>
								<p class="text-sm font-medium text-red-800">Analysis Error</p>
								<p class="text-sm text-red-700 mt-1">{error}</p>
							</div>
						</div>
					{/if}

					<div class="space-y-2">
						<Button 
							class="w-full" 
							on:click={handleAnalyze} 
							
						>
							{#if isLoading}
								<Loader class="mr-2 h-4 w-4 animate-spin" />
								Analyzing...
							{:else}
								Analyze
							{/if}
						</Button>
						
						<div class="flex items-center justify-between">
							<div class="text-xs text-gray-500">
								{#if !isBackendAvailable}
									<span class="text-red-500">Backend unavailable</span>
								{:else if !content.trim()}
									Enter some text to analyze
								{:else}
									Ready to analyze
								{/if}
							</div>
							
							{#if isBackendAvailable}
								<div class="flex items-center text-xs text-green-600">
									<CheckCircle2 class="h-3 w-3 mr-1" />
									<span>Backend connected</span>
								</div>
							{/if}
						</div>
					</div>
				</div>
			</CardContent>
		</Card>
	{/if}
</div>
