<script lang="ts">
import type { Snippet } from 'svelte';
import { buttonVariants, cn, uiTokens } from '$lib/theme';

type Variant = keyof typeof buttonVariants;
type Size = 'sm' | 'md' | 'lg';

interface Props {
	variant?: Variant;
	size?: Size;
	loading?: boolean;
	className?: string;
	fullWidth?: boolean;
	href?: string;
	disabled?: boolean;
	type?: 'button' | 'submit' | 'reset';
	onclick?: (e: MouseEvent) => void;
	children?: Snippet;
}

let {
	variant = 'primary',
	size = 'md',
	loading = false,
	className = '',
	fullWidth = false,
	href,
	disabled = false,
	type = 'button',
	onclick,
	children
}: Props = $props();

const sizeClasses: Record<Size, string> = {
	sm: 'px-3 py-1.5 text-sm',
	md: 'px-4 py-2 text-sm',
	lg: 'px-5 py-2.5 text-base'
};

const classes = $derived(cn(
	'inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-colors disabled:cursor-not-allowed',
	sizeClasses[size],
	buttonVariants[variant],
	uiTokens.focusRing,
	fullWidth && 'w-full',
	className
));
</script>

{#if href}
	<a {href} class={classes}>
		{#if loading}
			<span class="size-4 animate-spin rounded-full border-2 border-current border-r-transparent" aria-hidden="true"></span>
		{/if}
		{@render children?.()}
	</a>
{:else}
	<button
		{type}
		class={classes}
		disabled={disabled || loading}
		{onclick}
	>
		{#if loading}
			<span class="size-4 animate-spin rounded-full border-2 border-current border-r-transparent" aria-hidden="true"></span>
		{/if}
		{@render children?.()}
	</button>
{/if}
