<script lang="ts">
	import Button from '$lib/components/ui/button.svelte';
	import Card from '$lib/components/ui/card.svelte';
	import CardContent from '$lib/components/ui/card-content.svelte';
	import ResultCard from '$lib/components/ResultCard.svelte';
	import { resetAnalysis } from '$lib/stores/analysisStore';
	import type { AnalysisResult } from '$lib/stores/analysisStore';

	let {
		results,
		class: className = ''
	}: {
		results: AnalysisResult;
		class?: string;
	} = $props();

	let showOriginalContent = $state(false);

	function getTrustScoreColor(score: number): string {
		if (score >= 71) return 'text-green-700';
		if (score >= 41) return 'text-amber-600';
		return 'text-red-700';
	}

	function getTrustScoreBgColor(score: number): string {
		if (score >= 71) return 'bg-green-100';
		if (score >= 41) return 'bg-amber-100';
		return 'bg-red-100';
	}

	function getTrustScoreLabel(score: number): string {
		if (score >= 71) return 'High Trust';
		if (score >= 41) return 'Medium Trust';
		return 'Low Trust';
	}
</script>

<div class="space-y-6 {className}">
	<!-- Trust Score Display -->
	<Card class="text-center">
		<CardContent class="p-8">
			<div class="mb-4">
				<div
					class="mx-auto h-32 w-32 rounded-full {getTrustScoreBgColor(
						results.trust_score
					)} mb-4 flex items-center justify-center"
				>
					<span class="text-4xl font-bold {getTrustScoreColor(results.trust_score)}">
						{results.trust_score}%
					</span>
				</div>
				<h2 class="mb-2 text-2xl font-bold text-slate-800">
					{getTrustScoreLabel(results.trust_score)}
				</h2>
				<p class="text-lg text-slate-600">
					{results.result_summary}
				</p>
			</div>
		</CardContent>
	</Card>

	<!-- Original Content Toggle -->
	<Card>
		<CardContent class="p-4">
			<button
				class="text-sm font-medium text-blue-600 hover:text-blue-700"
				onclick={() => (showOriginalContent = !showOriginalContent)}
			>
				{showOriginalContent ? 'Hide' : 'Show'} Analyzed Content
			</button>
			{#if showOriginalContent}
				<div class="mt-3 rounded-md bg-slate-50 p-3">
					<pre class="text-sm whitespace-pre-wrap text-slate-700">{results.original_content}</pre>
				</div>
			{/if}
		</CardContent>
	</Card>

	<!-- Educational Breakdown -->
	<div class="space-y-4">
		<h3 class="text-xl font-bold text-slate-800">Analysis Breakdown</h3>
		<div class="space-y-3">
			{#each results.educational_breakdown as item}
				<ResultCard {item} />
			{/each}
		</div>
	</div>

	<!-- Start New Analysis Button -->
	<div class="pt-6">
		<Button class="w-full" onclick={resetAnalysis}>Start New Analysis</Button>
	</div>
</div>
