<script lang="ts">
	import { Badge, Button, Card, SectionHeader } from '$lib/components';
	import { cn, uiTokens } from '$lib/theme';

	// Define the two unified tracks with their categories and modules
	const tracks = [
		{
			id: 'everyday',
			title: 'Everyday Security',
			description: 'Protect yourself from common online threats with practical skills anyone can learn.',
			icon: '🛡️',
			color: 'success',
			href: '/tracks/everyday',
			difficulty: 'Beginner',
			moduleCount: 4,
			availableCount: 2,
			categories: [
				{
					name: 'Recognizing Threats',
					modules: ['Phishing Attacks', 'Social Engineering']
				},
				{
					name: 'Best Practices',
					modules: ['Password Security', 'Safe Browsing']
				}
			]
		},
		{
			id: 'developer',
			title: 'Developer Security',
			description: 'Learn to build secure applications and protect against common web vulnerabilities.',
			icon: '💻',
			color: 'brand',
			href: '/tracks/developer',
			difficulty: 'Intermediate',
			moduleCount: 5,
			availableCount: 3,
			categories: [
				{
					name: 'Web Vulnerabilities',
					modules: ['Cross-Site Scripting (XSS)', 'SQL Injection', 'CSRF']
				},
				{
					name: 'Secure Development',
					modules: ['Authentication Security', 'API Security']
				}
			]
		}
	];

	const colorStyles = {
		success: {
			bg: 'bg-success-soft',
			border: 'border-success-border',
			text: 'text-success',
			button: 'bg-success hover:bg-success/90'
		},
		brand: {
			bg: 'bg-brand-soft',
			border: 'border-brand-border',
			text: 'text-brand',
			button: 'bg-brand hover:bg-brand-strong'
		}
	};
</script>

<svelte:head>
	<title>Learning Tracks | CyberLearn</title>
	<meta name="description" content="Choose your cybersecurity learning path: Everyday Security for everyone, or Developer Security for building secure applications." />
</svelte:head>

<SectionHeader 
	title="Learning Tracks" 
	subtitle="Choose your path to cybersecurity mastery. Each track contains categorized modules with interactive demos."
>
	{#snippet actions()}
		<Button variant="secondary" href="/">Back to Dashboard</Button>
	{/snippet}
</SectionHeader>

<!-- Track Selection -->
<div class="grid gap-6 md:grid-cols-2 mb-8">
	{#each tracks as track (track.id)}
		{@const styles = colorStyles[track.color as keyof typeof colorStyles]}
		<a
			href={track.href}
			class={cn(
				uiTokens.cardHover,
				"block p-6 group",
				styles.border
			)}
		>
			<div class="flex items-start justify-between gap-4 mb-4">
				<div class="flex items-center gap-3">
					<div class={cn("size-12 rounded-xl flex items-center justify-center text-2xl", styles.bg)}>
						{track.icon}
					</div>
					<div>
						<h2 class="text-xl font-bold text-text">{track.title}</h2>
						<Badge variant={track.color as 'success' | 'brand'}>{track.difficulty}</Badge>
					</div>
				</div>
			</div>
			
			<p class="text-sm text-text-muted mb-4">{track.description}</p>
			
			<!-- Categories Preview -->
			<div class="space-y-3 mb-4">
				{#each track.categories as category}
					<div>
						<p class={cn("text-xs font-semibold uppercase tracking-wider mb-1.5", styles.text)}>
							{category.name}
						</p>
						<div class="flex flex-wrap gap-1.5">
							{#each category.modules as module}
								<span class="px-2 py-1 text-xs rounded-md bg-muted border border-border text-text-muted">
									{module}
								</span>
							{/each}
						</div>
					</div>
				{/each}
			</div>
			
			<!-- Progress indicator -->
			<div class="flex items-center justify-between text-sm">
				<span class="text-text-muted">{track.availableCount} of {track.moduleCount} modules available</span>
				<span class={cn("font-medium group-hover:underline", styles.text)}>
					Explore Track →
				</span>
			</div>
		</a>
	{/each}
</div>

<!-- Quick Access to All Interactive Modules -->
<Card className="mb-8">
	<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
		<div>
			<h3 class="text-lg font-semibold text-text">Interactive Modules Hub</h3>
			<p class="text-sm text-text-muted">Browse all available interactive demos in one place</p>
		</div>
		<a 
			href="/modules"
			class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-brand text-white font-medium hover:bg-brand-strong transition-colors"
		>
			<svg class="size-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
			</svg>
			View All Modules
		</a>
	</div>
	
	<div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
		<a href="/modules/phishing" class={cn(uiTokens.cardHover, "p-3 text-center")}>
			<span class="text-2xl mb-1 block">🎣</span>
			<span class="text-sm font-medium text-text">Phishing</span>
		</a>
		<a href="/modules/password-security" class={cn(uiTokens.cardHover, "p-3 text-center")}>
			<span class="text-2xl mb-1 block">🔐</span>
			<span class="text-sm font-medium text-text">Passwords</span>
		</a>
		<a href="/modules/xss" class={cn(uiTokens.cardHover, "p-3 text-center")}>
			<span class="text-2xl mb-1 block">💉</span>
			<span class="text-sm font-medium text-text">XSS</span>
		</a>
		<a href="/modules/sql-injection" class={cn(uiTokens.cardHover, "p-3 text-center")}>
			<span class="text-2xl mb-1 block">🗄️</span>
			<span class="text-sm font-medium text-text">SQL Injection</span>
		</a>
		<a href="/modules/csrf" class={cn(uiTokens.cardHover, "p-3 text-center")}>
			<span class="text-2xl mb-1 block">🎯</span>
			<span class="text-sm font-medium text-text">CSRF</span>
		</a>
	</div>
</Card>

<!-- Learning Path Recommendations -->
<Card>
	<div class="flex items-start gap-4">
		<div class="size-10 rounded-lg bg-warning-soft flex items-center justify-center flex-shrink-0">
			<span class="text-xl">💡</span>
		</div>
		<div>
			<h3 class="font-semibold text-text mb-2">Which Track Should I Choose?</h3>
			<div class="space-y-3 text-sm text-text-muted">
				<p>
					<span class="font-medium text-success">Everyday Security</span> is perfect if you want to protect yourself online. 
					Learn to spot scams, create strong passwords, and browse safely - no technical knowledge required.
				</p>
				<p>
					<span class="font-medium text-brand">Developer Security</span> is for developers who want to build secure applications. 
					Learn about XSS, SQL injection, CSRF, and other vulnerabilities through hands-on demos.
				</p>
			</div>
		</div>
	</div>
</Card>
