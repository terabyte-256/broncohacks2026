<script lang="ts">
	import type { Snippet } from 'svelte';
	import { cn, uiTokens } from '$lib/theme';

	interface Props {
		title?: string;
		description?: string;
		className?: string;
		muted?: boolean;
		children?: Snippet;
		header?: Snippet;
		footer?: Snippet;
	}

let { title, description, className = '', muted = false, children, header, footer }: Props = $props();
</script>

<article class={cn(muted ? uiTokens.cardMuted : uiTokens.card, className)}>
{#if title || description || header}
<header class="border-b border-border px-5 py-4">
{#if header}
{@render header()}
{:else}
{#if title}
<h3 class="text-base font-semibold text-text">{title}</h3>
{/if}
{#if description}
<p class="mt-1 text-sm text-text-muted">{description}</p>
{/if}
{/if}
</header>
{/if}
<div class="px-5 py-4">
{@render children?.()}
</div>
{#if footer}
<footer class="border-t border-border px-5 py-4">
{@render footer()}
</footer>
{/if}
</article>
