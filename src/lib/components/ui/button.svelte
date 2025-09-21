<script lang="ts">
	import { cn } from '$lib/utils';

	type Variant = 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
	type Size = 'default' | 'sm' | 'lg' | 'icon';

	let {
		variant = 'default',
		size = 'default',
		class: className = '',
		disabled = false,
		children,
		...restProps
	}: {
		variant?: Variant;
		size?: Size;
		class?: string;
		disabled?: boolean;
		children?: any;
		[key: string]: any;
	} = $props();

	const variants = {
		default: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
		destructive: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
		outline: 'border border-slate-300 bg-transparent hover:bg-slate-100 focus:ring-blue-500',
		secondary: 'bg-slate-100 text-slate-800 hover:bg-slate-200 focus:ring-blue-500',
		ghost: 'hover:bg-slate-100 focus:ring-blue-500',
		link: 'text-blue-600 underline-offset-4 hover:underline focus:ring-blue-500'
	};

	const sizes = {
		default: 'h-10 px-4 py-2',
		sm: 'h-9 px-3',
		lg: 'h-11 px-8',
		icon: 'h-10 w-10'
	};
</script>

<button
	class={cn(
		'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50',
		variants[variant],
		sizes[size],
		className
	)}
	{disabled}
	{...restProps}
	onclick={() => restProps.onClick?.()}
>
	{@render children?.()}
</button>
