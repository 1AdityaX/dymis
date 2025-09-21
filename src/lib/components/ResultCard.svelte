<script lang="ts">
	import Card from '$lib/components/ui/card.svelte';
	import CardContent from '$lib/components/ui/card-content.svelte';
	import type { EducationalBreakdown } from '$lib/stores/analysisStore';

	let {
		item,
		class: className = ''
	}: {
		item: EducationalBreakdown;
		class?: string;
	} = $props();
</script>

<Card class="transition-shadow hover:shadow-md {className}">
	<CardContent class="p-4">
		<div class="flex items-start gap-3">
			<div class="mt-1 flex-shrink-0">
				<div class="flex h-8 w-8 items-center justify-center rounded-full bg-amber-100">
					<span class="text-lg text-amber-600">⚠️</span>
				</div>
			</div>
			<div class="min-w-0 flex-1">
				<h3 class="mb-2 text-base font-bold text-slate-800">
					{item.title}
				</h3>
				<p class="mb-3 text-sm leading-relaxed text-slate-600">
					{item.explanation}
				</p>
				{#if item.quote}
					<blockquote
						class="border-l-4 border-slate-300 bg-slate-50 py-2 pl-3 text-sm text-slate-700 italic"
					>
						"{item.quote}"
					</blockquote>
				{/if}
			</div>
		</div>
	</CardContent>
</Card>
