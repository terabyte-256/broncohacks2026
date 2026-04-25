<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		title: string;
		subtitle?: string;
		children?: Snippet;
		actions?: Snippet;
	}

let { title, subtitle = '', children, actions }: Props = $props();
</script>

<header class="mb-5 flex flex-wrap items-start justify-between gap-3">
<div>
<h1 class="text-2xl font-semibold text-text">{title}</h1>
{#if subtitle}
<p class="mt-1 text-sm text-text-muted">{subtitle}</p>
{/if}
{#if children}
<div class="mt-3">{@render children()}</div>
{/if}
</div>
{#if actions}
<div class="flex items-center gap-2">{@render actions()}</div>
{/if}
</header>
