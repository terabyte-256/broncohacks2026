<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import { getDashboard } from '$lib/services';
	import { cn, uiTokens } from '$lib/theme';

	let { children } = $props();

	let streakDays = $state(0);
	let averageScore = $state(0);

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

	onMount(async () => {
		try {
			const dashboard = await getDashboard();
			streakDays = dashboard.metrics.streakDays;
			averageScore = dashboard.metrics.averageQuizScore;
		} catch {
			// silent — display-only metrics
		}
	});
</script>

<div class="min-h-screen bg-canvas">
	<header class="border-b border-border bg-surface/95 backdrop-blur">
		<div class={cn(uiTokens.pageWidth, 'flex flex-wrap items-center justify-between gap-3 py-4')}>
			<div class="flex items-center gap-2">
				<span class="text-xl">🔒</span>
				<div>
					<p class="text-lg font-semibold text-text">CyberLearn</p>
					<p class="text-xs text-text-muted">AI-powered security training</p>
				</div>
			</div>
			<div class="flex items-center gap-2">
				<div class="flex items-center gap-1.5 rounded-lg border border-border bg-muted px-3 py-1.5">
					<span>⭐</span>
					<span class="text-sm font-semibold text-text">{averageScore}</span>
					<span class="text-xs text-text-muted">Score</span>
				</div>
				<div class="flex items-center gap-1.5 rounded-lg border border-border bg-muted px-3 py-1.5">
					<span>🔥</span>
					<span class="text-sm font-semibold text-text">{streakDays}</span>
					<span class="text-xs text-text-muted">Streak</span>
				</div>
			</div>
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
