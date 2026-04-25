<script lang="ts">
	import type { Snippet } from 'svelte';
	import { alertVariants, cn } from '$lib/theme';

type Variant = keyof typeof alertVariants;

	interface Props {
		variant?: Variant;
		title?: string;
		className?: string;
		children?: Snippet;
	}

let { variant = 'info', title = '', className = '', children }: Props = $props();
</script>

<div class={cn('rounded-lg border px-4 py-3 text-sm', alertVariants[variant], className)} role="status" aria-live="polite">
{#if title}
<p class="font-semibold">{title}</p>
{/if}
<div class={title ? 'mt-1' : ''}>
{@render children?.()}
</div>
</div>
