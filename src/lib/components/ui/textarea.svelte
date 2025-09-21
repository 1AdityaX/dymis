<script lang="ts">
	import { cn } from '$lib/utils';

	let {
		class: className = '',
		disabled = false,
		value = $bindable(),
		children,
		...restProps
	}: {
		class?: string;
		disabled?: boolean;
		value?: string;
		children?: any;
		[key: string]: any;
	} = $props();
</script>

<textarea
	class={cn(
		'flex min-h-[80px] w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm placeholder:text-slate-500 focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50',
		className
	)}
	{disabled}
	{value}
	{...restProps}
></textarea>
