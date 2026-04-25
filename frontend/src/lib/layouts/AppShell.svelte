<script lang="ts">
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import { defaultUser } from '$lib/stores';
	import { Badge } from '$lib/components';
import { cn, uiTokens } from '$lib/theme';

let { children } = $props();

	const navItems = [
		{ href: '/', label: 'Dashboard', match: '/' },
		{ href: '/tracks', label: 'Tracks', match: '/tracks' },
		{ href: '/quiz', label: 'Quiz', match: '/quiz' },
		{ href: '/message-checker', label: 'Message Checker', match: '/message-checker' },
		{ href: '/history', label: 'History', match: '/history' }
	] as const;

	function isActive(match: string): boolean {
		return match === '/'
			? page.url.pathname === '/'
			: page.url.pathname === match || page.url.pathname.startsWith(`${match}/`);
	}
</script>

<div class="min-h-screen bg-canvas">
<header class="border-b border-border bg-surface/95 backdrop-blur">
<div class={cn(uiTokens.pageWidth, 'flex flex-wrap items-center justify-between gap-3 py-4')}>
<div>
<p class="text-lg font-semibold text-text">CyberLearn</p>
<p class="text-xs text-text-muted">Frontend prototype for a single default learner</p>
</div>
<Badge variant="brand">{$defaultUser.displayName}</Badge>
</div>
<nav class="border-t border-border">
<div class={cn(uiTokens.pageWidth, 'flex flex-wrap gap-2 py-3')}>
				{#each navItems as item (item.href)}
					<a
						href={resolve(item.href)}
						class={cn(
							'rounded-md px-3 py-2 text-sm transition-colors',
							isActive(item.match)
								? 'bg-brand-soft text-brand-strong'
								: 'text-text-muted hover:bg-muted hover:text-text'
						)}
					>
{item.label}
</a>
{/each}
</div>
</nav>
</header>

<main class={cn(uiTokens.pageWidth, 'py-6')}>
{@render children()}
</main>
</div>
