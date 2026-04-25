<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { goto, invalidateAll } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { getDashboard } from '$lib/services';
	import { createClient } from '$lib/supabase/client';
	import { cn, uiTokens } from '$lib/theme';
	import type { User } from '@supabase/supabase-js';

	interface Props {
		children: import('svelte').Snippet;
		user: User | null;
	}

	let { children, user }: Props = $props();

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

	async function handleSignOut() {
		const supabase = createClient();
		await supabase.auth.signOut();
		await invalidateAll();
		goto('/');
	}

	// Get display name from user metadata
	const displayName = $derived(
		user?.user_metadata?.full_name || 
		user?.user_metadata?.name || 
		user?.email?.split('@')[0] || 
		'User'
	);

	const avatarUrl = $derived(user?.user_metadata?.avatar_url);

	onMount(async () => {
		if (!user) return;
		
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
			<a href="/" class="flex items-center gap-2 transition-opacity hover:opacity-80">
				<span class="text-xl">🔒</span>
				<div>
					<p class="text-lg font-semibold text-text">CyberLearn</p>
					<p class="text-xs text-text-muted">AI-powered security training</p>
				</div>
			</a>
			
			<div class="flex items-center gap-3">
				{#if user}
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
					
					<div class="flex items-center gap-2">
						{#if avatarUrl}
							<img 
								src={avatarUrl} 
								alt={displayName}
								class="h-8 w-8 rounded-full border border-border"
							/>
						{:else}
							<div class="flex h-8 w-8 items-center justify-center rounded-full bg-brand text-sm font-medium text-white">
								{displayName.charAt(0).toUpperCase()}
							</div>
						{/if}
						<span class="hidden text-sm text-text sm:inline">{displayName}</span>
						<button
							onclick={handleSignOut}
							class="rounded-md px-3 py-1.5 text-sm text-text-muted transition-colors hover:bg-muted hover:text-text"
						>
							Sign Out
						</button>
					</div>
				{:else}
					<a
						href="/auth/login"
						class="rounded-md bg-brand px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-brand-strong"
					>
						Sign In
					</a>
				{/if}
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
