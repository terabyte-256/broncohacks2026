<script lang="ts">
	import { onMount } from 'svelte';
	import { Alert, Badge, Button, Card, ProgressBar, SectionHeader } from '$lib/components';
	import {
		getErrorMessage,
		getTrackModules,
		getTracks,
		type TrackModulesResponse,
		type TrackSummary
	} from '$lib/services';
	import { createAsyncState } from '$lib/stores';
	import { cn, uiTokens } from '$lib/theme';

	// Module link mapping - connects backend modules to interactive demos
	const moduleLinks: Record<string, { href: string; label: string }> = {
		'xss': { href: '/modules/xss', label: 'Try XSS Demo' },
		'sql-injection': { href: '/modules/sql-injection', label: 'Try SQL Injection Demo' },
		'csrf': { href: '/modules/csrf', label: 'Try CSRF Demo' },
		'phishing': { href: '/modules/phishing', label: 'Try Phishing Demo' },
		'password-security': { href: '/modules/password-security', label: 'Try Password Demo' },
		'social-engineering': { href: '/modules/social-engineering', label: 'Coming Soon' },
		'safe-browsing': { href: '/modules/safe-browsing', label: 'Coming Soon' }
	};

	// Match module titles to their keys
	function getModuleKey(title: string): string | null {
		const titleLower = title.toLowerCase();
		if (titleLower.includes('xss') || titleLower.includes('cross-site scripting')) return 'xss';
		if (titleLower.includes('sql injection')) return 'sql-injection';
		if (titleLower.includes('csrf') || titleLower.includes('request forgery')) return 'csrf';
		if (titleLower.includes('phishing')) return 'phishing';
		if (titleLower.includes('password')) return 'password-security';
		if (titleLower.includes('social engineering')) return 'social-engineering';
		if (titleLower.includes('browsing') || titleLower.includes('safe')) return 'safe-browsing';
		return null;
	}

	const tracksState = createAsyncState<TrackSummary[]>();
	const modulesState = createAsyncState<TrackModulesResponse>();

	let selectedTrackId = $state<number | null>(null);

	async function loadTracks() {
		tracksState.setLoading();
		try {
			const response = await getTracks();
			if (!response.tracks.length) {
				tracksState.setEmpty('No learning tracks available yet.');
				modulesState.reset();
				selectedTrackId = null;
				return;
			}
			tracksState.setSuccess(response.tracks);
			const nextTrackId = selectedTrackId ?? response.tracks[0].id;
			await loadModules(nextTrackId);
		} catch (error) {
			tracksState.setError(getErrorMessage(error));
		}
	}

	async function loadModules(trackId: number) {
		selectedTrackId = trackId;
		modulesState.setLoading();
		try {
			const response = await getTrackModules(trackId);
			if (!response.modules.length) {
				modulesState.setEmpty('This track has no modules yet.');
				return;
			}
			modulesState.setSuccess(response);
		} catch (error) {
			modulesState.setError(getErrorMessage(error));
		}
	}

	onMount(() => {
		void loadTracks();
	});
</script>

<svelte:head>
	<title>Learning Tracks | CyberLearn</title>
	<meta name="description" content="Browse cybersecurity learning tracks and track your progress through modules and quizzes." />
</svelte:head>

<SectionHeader title="Learning Tracks" subtitle="Browse tracks and track your module-level progress. Click on a module to try the interactive demo.">
	{#snippet actions()}
		<div class="flex items-center gap-2">
			<a href="/modules" class="text-sm text-brand hover:underline">View All Modules</a>
			<Button variant="secondary" onclick={loadTracks}>Reload Tracks</Button>
		</div>
	{/snippet}
</SectionHeader>

<!-- Quick Access to Interactive Modules -->
<div class="mb-6 p-4 rounded-xl bg-brand-soft border border-brand-border">
	<div class="flex items-center gap-3 mb-3">
		<div class="size-10 rounded-lg bg-brand flex items-center justify-center">
			<svg class="size-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
			</svg>
		</div>
		<div>
			<h3 class="font-semibold text-text">Interactive Demos Available</h3>
			<p class="text-sm text-text-muted">Try hands-on security demos in the Modules section</p>
		</div>
	</div>
	<div class="flex flex-wrap gap-2">
		<a href="/modules/xss" class="px-3 py-1.5 text-sm rounded-lg bg-surface border border-border hover:border-brand-border transition-colors">XSS Demo</a>
		<a href="/modules/sql-injection" class="px-3 py-1.5 text-sm rounded-lg bg-surface border border-border hover:border-brand-border transition-colors">SQL Injection Demo</a>
		<a href="/modules/csrf" class="px-3 py-1.5 text-sm rounded-lg bg-surface border border-border hover:border-brand-border transition-colors">CSRF Demo</a>
		<a href="/modules/phishing" class="px-3 py-1.5 text-sm rounded-lg bg-surface border border-border hover:border-brand-border transition-colors">Phishing Demo</a>
		<a href="/modules/password-security" class="px-3 py-1.5 text-sm rounded-lg bg-surface border border-border hover:border-brand-border transition-colors">Password Demo</a>
	</div>
</div>

<div class="grid gap-5 lg:grid-cols-[2fr_3fr]">
	<Card title="Tracks" description="Select a track to inspect modules and quizzes.">
		{#if $tracksState.status === 'loading'}
			<p class="text-sm text-text-muted">Loading tracks...</p>
		{:else if $tracksState.status === 'error'}
			<Alert variant="danger">{$tracksState.message}</Alert>
		{:else if $tracksState.status === 'empty'}
			<Alert variant="warning">{$tracksState.message}</Alert>
		{:else if $tracksState.status === 'success' && $tracksState.data}
			<ul class="space-y-3">
				{#each $tracksState.data as track (track.id)}
					<li>
						<button
							type="button"
							class={cn(
								"w-full rounded-lg border px-3 py-3 text-left transition-colors",
								selectedTrackId === track.id
									? 'border-brand-border bg-brand-soft'
									: 'border-border bg-surface hover:bg-muted'
							)}
							onclick={() => loadModules(track.id)}
						>
							<div class="flex flex-wrap items-center justify-between gap-2">
								<p class="font-medium text-text">{track.title}</p>
								<Badge variant={track.completionPercent >= 100 ? 'success' : 'neutral'}>{track.completionPercent}%</Badge>
							</div>
							<p class="mt-1 text-sm text-text-muted">{track.description}</p>
							<div class="mt-2 text-xs text-text-muted">
								{track.completedModules}/{track.moduleCount} modules completed
							</div>
						</button>
					</li>
				{/each}
			</ul>
		{/if}
	</Card>

	<Card title="Modules" description="Modules for the selected track. Click to try interactive demos.">
		{#if $modulesState.status === 'loading'}
			<p class="text-sm text-text-muted">Loading modules...</p>
		{:else if $modulesState.status === 'error'}
			<Alert variant="danger">{$modulesState.message}</Alert>
		{:else if $modulesState.status === 'empty'}
			<Alert variant="warning">{$modulesState.message}</Alert>
		{:else if $modulesState.status === 'success' && $modulesState.data}
			<div class="space-y-3">
				<p class="text-sm text-text-muted">{$modulesState.data.track.title}</p>
				<ul class="space-y-3">
					{#each $modulesState.data.modules as module (module.id)}
						{@const moduleKey = getModuleKey(module.title)}
						{@const link = moduleKey ? moduleLinks[moduleKey] : null}
						<li class="rounded-lg border border-border bg-muted px-3 py-3">
							<div class="flex flex-wrap items-center justify-between gap-2">
								<p class="font-medium text-text">{module.title}</p>
								<Badge variant={module.completed ? 'success' : 'brand'}>{module.completed ? 'completed' : 'in progress'}</Badge>
							</div>
							<p class="mt-1 text-sm text-text-muted">{module.description}</p>
							<div class="mt-2">
								<ProgressBar value={module.completionPercent} label={`${module.title} completion`} />
							</div>
							{#if module.lastScore !== null}
								<p class="mt-2 text-xs text-text-muted">Last quiz score: {module.lastScore}%</p>
							{/if}
							
							<!-- Interactive Demo Link -->
							{#if link && !link.label.includes('Coming Soon')}
								<a 
									href={link.href}
									class="mt-3 inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium rounded-lg bg-brand text-white hover:bg-brand-strong transition-colors"
								>
									<svg class="size-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
									</svg>
									{link.label}
								</a>
							{:else if link}
								<span class="mt-3 inline-flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-lg bg-muted text-text-muted">
									<svg class="size-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
									</svg>
									Demo Coming Soon
								</span>
							{/if}
						</li>
					{/each}
				</ul>
			</div>
		{:else}
			<Alert variant="info">Choose a track to view modules.</Alert>
		{/if}
	</Card>
</div>
