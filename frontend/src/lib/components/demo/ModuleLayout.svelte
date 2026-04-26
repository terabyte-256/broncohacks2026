<script lang="ts">
	import type { Snippet } from 'svelte';
	import { cn, uiTokens } from '$lib/theme';
	import { Button, Badge, ProgressBar } from '$lib/components';

	interface Props {
		title: string;
		subtitle: string;
		icon: string;
		difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
		estimatedTime: string;
		track?: 'everyday' | 'developer';
		progress?: number;
		className?: string;
		children?: Snippet;
		quiz?: Snippet;
	}

	let { title, subtitle, icon, difficulty, estimatedTime, track, progress = 0, className = '', children, quiz }: Props = $props();

	const difficultyColors = {
		'Beginner': 'success',
		'Intermediate': 'warning', 
		'Advanced': 'danger'
	} as const;

	const trackLabels = {
		'everyday': { label: 'Everyday Security', color: 'bg-success-soft text-success border-success-border' },
		'developer': { label: 'Developer Security', color: 'bg-brand-soft text-brand border-brand-border' }
	} as const;

	let activeSection = $state<'learn' | 'quiz'>('learn');
</script>

<div class={cn(uiTokens.pageWidth, "py-8", className)}>
	<!-- Header -->
	<header class="mb-8">
		<a href="/modules" class="inline-flex items-center gap-2 text-sm text-text-muted hover:text-text transition-colors mb-4">
			<svg class="size-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
			</svg>
			Back to Modules
		</a>
		
		<div class="flex items-start gap-4">
			<div class="size-16 rounded-xl bg-brand-soft flex items-center justify-center text-3xl">
				{icon}
			</div>
			
			<div class="flex-1">
				<div class="flex flex-wrap items-center gap-3 mb-1">
					<h1 class="text-2xl font-bold text-text">{title}</h1>
					<Badge variant={difficultyColors[difficulty]}>{difficulty}</Badge>
					{#if track}
						<span class={cn("px-2 py-0.5 text-xs rounded-full border", trackLabels[track].color)}>
							{trackLabels[track].label}
						</span>
					{/if}
				</div>
				<p class="text-text-muted">{subtitle}</p>
				
				<div class="flex items-center gap-4 mt-3 text-sm text-text-muted">
					<span class="flex items-center gap-1.5">
						<svg class="size-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
						{estimatedTime}
					</span>
					{#if progress > 0}
						<span class="flex items-center gap-2">
							<ProgressBar value={progress} max={100} size="sm" className="w-24" />
							<span>{progress}% complete</span>
						</span>
					{/if}
				</div>
			</div>
		</div>
	</header>

	<!-- Section Tabs -->
	{#if quiz}
		<div class="flex gap-2 mb-6 border-b border-border pb-2">
			<button 
				class={cn(
					"px-4 py-2 text-sm font-medium rounded-t-lg transition-colors",
					activeSection === 'learn' 
						? "text-brand border-b-2 border-brand -mb-[2px]" 
						: "text-text-muted hover:text-text"
				)}
				onclick={() => activeSection = 'learn'}
			>
				Learn
			</button>
			<button 
				class={cn(
					"px-4 py-2 text-sm font-medium rounded-t-lg transition-colors",
					activeSection === 'quiz' 
						? "text-brand border-b-2 border-brand -mb-[2px]" 
						: "text-text-muted hover:text-text"
				)}
				onclick={() => activeSection = 'quiz'}
			>
				Knowledge Check
			</button>
		</div>
	{/if}

	<!-- Content -->
	{#if activeSection === 'learn'}
		<div class="space-y-8">
			{@render children?.()}
		</div>
	{:else if quiz}
		<div>
			{@render quiz()}
		</div>
	{/if}
</div>
