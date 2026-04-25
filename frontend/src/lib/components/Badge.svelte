<script lang="ts">
	import type { Snippet } from 'svelte';
	import { badgeVariants, cn } from '$lib/theme';

type Variant = keyof typeof badgeVariants;

	interface Props {
		variant?: Variant;
		className?: string;
		children?: Snippet;
	}

let { variant = 'neutral', className = '', children }: Props = $props();
</script>

<span
class={cn(
'inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium leading-none',
badgeVariants[variant],
className
)}
>
{@render children?.()}
</span>
