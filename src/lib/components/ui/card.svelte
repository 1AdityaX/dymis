<script lang="ts">
	import { cn } from '$lib/utils';

	let {
		class: className = '',
		children,
		...restProps
	}: {
		class?: string;
		children?: any;
		[key: string]: any;
	} = $props();
</script>

<div
	class={cn('rounded-lg border border-slate-200 bg-white text-slate-950 shadow-sm', className)}
	{...restProps}
>
	{@render children?.()}
</div>
