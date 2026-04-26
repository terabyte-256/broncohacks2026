<script lang="ts">
	import {
		Button,
		Card,
		SectionHeader,
		Badge,
	} from "$lib/components";
	import { cn, uiTokens } from "$lib/theme";

	// Developer Security modules with categories
	const categories = [
		{
			id: 'web-vulnerabilities',
			title: 'Web Vulnerabilities',
			description: 'Understand common attack vectors in web applications',
			modules: [
				{
					id: 'xss',
					title: 'Cross-Site Scripting (XSS)',
					description: 'Learn how attackers inject malicious scripts and how to prevent it',
					icon: '💉',
					difficulty: 'Beginner',
					estimatedTime: '15 min',
					href: '/modules/xss',
					available: true
				},
				{
					id: 'sql-injection',
					title: 'SQL Injection',
					description: 'Understand how attackers manipulate database queries',
					icon: '🗄️',
					difficulty: 'Intermediate',
					estimatedTime: '20 min',
					href: '/modules/sql-injection',
					available: true
				},
				{
					id: 'csrf',
					title: 'Cross-Site Request Forgery',
					description: 'Learn how attackers trick users into unwanted actions',
					icon: '🎯',
					difficulty: 'Intermediate',
					estimatedTime: '15 min',
					href: '/modules/csrf',
					available: true
				}
			]
		},
		{
			id: 'secure-development',
			title: 'Secure Development',
			description: 'Best practices for building secure applications',
			modules: [
				{
					id: 'auth-security',
					title: 'Authentication Security',
					description: 'Implement secure login flows and session management',
					icon: '🔑',
					difficulty: 'Intermediate',
					estimatedTime: '25 min',
					href: '/modules/auth-security',
					available: false
				},
				{
					id: 'api-security',
					title: 'API Security',
					description: 'Secure your REST and GraphQL endpoints',
					icon: '🔌',
					difficulty: 'Advanced',
					estimatedTime: '30 min',
					href: '/modules/api-security',
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
	title="Developer Security"
	subtitle="Learn to build secure applications and protect against common web vulnerabilities."
>
	{#snippet actions()}
		<Button variant="secondary" href="/tracks">All Tracks</Button>
	{/snippet}
</SectionHeader>

<!-- Track Progress Overview -->
<Card className="mb-8 bg-brand-soft border-brand-border">
	<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
		<div>
			<p class="text-sm font-medium text-brand">Your Progress</p>
			<p class="text-2xl font-bold text-brand-strong">3 of 5 modules available</p>
		</div>
		<div class="flex items-center gap-2">
			<Badge variant="brand">Intermediate Track</Badge>
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
			
			<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
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
				Start with XSS to understand client-side attacks, then move to SQL Injection for server-side vulnerabilities. 
				CSRF builds on both concepts. Complete all three to unlock advanced modules.
			</p>
		</div>
	</div>
</Card>
