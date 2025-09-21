<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>Dymis - Analyze with clarity. Fight misinformation.</title>
</svelte:head>

<main class="min-h-screen bg-slate-50">
	<div class="mx-auto w-full max-w-3xl px-4 py-8">
		{@render children?.()}
	</div>
</main>
