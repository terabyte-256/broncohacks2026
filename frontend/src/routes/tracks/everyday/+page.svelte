<script lang="ts">
	import {
		Button,
		Card,
		SectionHeader,
		Badge,
	} from "$lib/components";
	import { cn, uiTokens } from "$lib/theme";

	// Everyday Security modules with categories
	const categories = [
		{
			id: 'threats',
			title: 'Recognizing Threats',
			description: 'Learn to identify common online attacks targeting everyday users',
			modules: [
				{
					id: 'phishing',
					title: 'Phishing Attacks',
					description: 'Identify fake emails, SMS, and social engineering attempts',
					icon: '🎣',
					difficulty: 'Beginner',
					estimatedTime: '15 min',
					href: '/modules/phishing',
					available: true
				},
				{
					id: 'social-engineering',
					title: 'Social Engineering',
					description: 'Recognize manipulation tactics used by attackers',
					icon: '🎭',
					difficulty: 'Beginner',
					estimatedTime: '15 min',
					href: '/modules/social-engineering',
					available: false
				}
			]
		},
		{
			id: 'best-practices',
			title: 'Best Practices',
			description: 'Essential habits for staying safe online',
			modules: [
				{
					id: 'password-security',
					title: 'Password Security',
					description: 'Create strong passwords and use two-factor authentication',
					icon: '🔐',
					difficulty: 'Beginner',
					estimatedTime: '15 min',
					href: '/modules/password-security',
					available: true
				},
				{
					id: 'safe-browsing',
					title: 'Safe Browsing',
					description: 'Identify malicious websites and browse securely',
					icon: '🌐',
					difficulty: 'Beginner',
					estimatedTime: '10 min',
					href: '/modules/safe-browsing',
					available: false
				}
			]
		}
	];

	const difficultyColors = {
		'Beginner': 'success',
		'Intermediate': 'warning',
		'Advanced': 'danger'
	} as const;
</script>

<SectionHeader
	title="Everyday Security"
	subtitle="Protect yourself from common online threats with practical skills anyone can learn."
>
	{#snippet actions()}
		<Button variant="secondary" href="/tracks">All Tracks</Button>
	{/snippet}
</SectionHeader>

<!-- Track Progress Overview -->
<Card className="mb-8 bg-success-soft border-success-border">
	<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
		<div>
			<p class="text-sm font-medium text-success">Your Progress</p>
			<p class="text-2xl font-bold text-success">2 of 4 modules available</p>
		</div>
		<div class="flex items-center gap-2">
			<Badge variant="success">Beginner Friendly</Badge>
		</div>
	</div>
</Card>

<!-- Categories -->
<div class="space-y-10">
	{#each categories as category (category.id)}
		<section>
			<div class="mb-4">
				<h2 class="text-xl font-bold text-text">{category.title}</h2>
				<p class="text-sm text-text-muted">{category.description}</p>
			</div>
			
			<div class="grid gap-4 sm:grid-cols-2">
				{#each category.modules as module (module.id)}
					{#if module.available}
						<a
							href={module.href}
							class={cn(uiTokens.cardHover, "block p-5 group")}
						>
							<div class="flex items-start justify-between gap-3 mb-3">
								<span class="text-2xl" aria-hidden="true">{module.icon}</span>
								<Badge variant={difficultyColors[module.difficulty as keyof typeof difficultyColors]}>
									{module.difficulty}
								</Badge>
							</div>
							
							<h3 class="font-semibold text-text mb-2">{module.title}</h3>
							<p class="text-sm text-text-muted mb-4">{module.description}</p>
							
							<div class="flex items-center justify-between text-xs text-text-muted">
								<span>{module.estimatedTime}</span>
								<span class="font-medium text-brand group-hover:underline">
									Start Module →
								</span>
							</div>
						</a>
					{:else}
						<div class={cn(uiTokens.card, "p-5 opacity-60")}>
							<div class="flex items-start justify-between gap-3 mb-3">
								<span class="text-2xl grayscale" aria-hidden="true">{module.icon}</span>
								<Badge variant="neutral">Coming Soon</Badge>
							</div>
							
							<h3 class="font-semibold text-text mb-2">{module.title}</h3>
							<p class="text-sm text-text-muted mb-4">{module.description}</p>
							
							<div class="flex items-center justify-between text-xs text-text-muted">
								<span>{module.estimatedTime}</span>
								<span class="text-text-muted">Not available yet</span>
							</div>
						</div>
					{/if}
				{/each}
			</div>
		</section>
	{/each}
</div>

<!-- Learning Path Note -->
<Card className="mt-10">
	<div class="flex items-start gap-4">
		<span class="text-2xl" aria-hidden="true">💡</span>
		<div>
			<h3 class="font-semibold text-text mb-1">Recommended Learning Path</h3>
			<p class="text-sm text-text-muted">
				Start with Password Security to establish strong foundations, then learn to spot Phishing attacks. 
				These skills work together to keep you safe in your daily online activities.
			</p>
		</div>
	</div>
</Card>
