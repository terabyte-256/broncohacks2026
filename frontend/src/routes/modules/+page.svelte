<script lang="ts">
	import { Card, Badge, Button, SectionHeader, ProgressBar } from '$lib/components';
	import { cn, uiTokens } from '$lib/theme';

	interface Module {
		id: string;
		title: string;
		description: string;
		icon: string;
		difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
		estimatedTime: string;
		topics: string[];
		href: string;
		progress?: number;
	}

	const modules: Module[] = [
		{
			id: 'xss',
			title: 'Cross-Site Scripting (XSS)',
			description: 'Learn how attackers inject malicious scripts into web pages and how to prevent it with proper output encoding and CSP.',
			icon: '💉',
			difficulty: 'Beginner',
			estimatedTime: '15 min',
			topics: ['Reflected XSS', 'Stored XSS', 'DOM-based XSS', 'Defense strategies'],
			href: '/modules/xss'
		},
		{
			id: 'sql-injection',
			title: 'SQL Injection',
			description: 'Understand how attackers manipulate database queries to access unauthorized data and how to use parameterized queries.',
			icon: '🗄️',
			difficulty: 'Intermediate',
			estimatedTime: '20 min',
			topics: ['In-band SQLi', 'Blind SQLi', 'Parameterized queries', 'ORM usage'],
			href: '/modules/sql-injection'
		},
		{
			id: 'csrf',
			title: 'Cross-Site Request Forgery',
			description: 'Discover how attackers trick users into performing unwanted actions and how CSRF tokens protect against these attacks.',
			icon: '🎭',
			difficulty: 'Intermediate',
			estimatedTime: '15 min',
			topics: ['CSRF attacks', 'Token validation', 'SameSite cookies', 'Origin headers'],
			href: '/modules/csrf'
		},
		{
			id: 'phishing',
			title: 'Phishing Attacks',
			description: 'Learn to identify and protect yourself from social engineering attacks via email, SMS, and other channels.',
			icon: '🎣',
			difficulty: 'Beginner',
			estimatedTime: '15 min',
			topics: ['Email phishing', 'Spear phishing', 'Red flags', 'Verification'],
			href: '/modules/phishing'
		},
		{
			id: 'password-security',
			title: 'Password Security',
			description: 'Understand how passwords are attacked and learn to create strong, secure passwords using best practices.',
			icon: '🔐',
			difficulty: 'Beginner',
			estimatedTime: '15 min',
			topics: ['Brute force', 'Dictionary attacks', 'Password managers', '2FA'],
			href: '/modules/password-security'
		}
	];

	const difficultyColors = {
		'Beginner': 'success',
		'Intermediate': 'warning',
		'Advanced': 'danger'
	} as const;

	let selectedDifficulty = $state<'All' | 'Beginner' | 'Intermediate' | 'Advanced'>('All');

	const filteredModules = $derived(
		selectedDifficulty === 'All' 
			? modules 
			: modules.filter(m => m.difficulty === selectedDifficulty)
	);
</script>

<svelte:head>
	<title>Security Modules | CyberLearn</title>
	<meta name="description" content="Interactive cybersecurity training modules covering XSS, SQL Injection, CSRF, Phishing, and more." />
</svelte:head>

<div class={cn(uiTokens.pageWidth, "py-8")}>
	<!-- Header -->
	<header class="mb-8">
		<a href="/" class="inline-flex items-center gap-2 text-sm text-text-muted hover:text-text transition-colors mb-4">
			<svg class="size-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
			</svg>
			Back to Dashboard
		</a>
		
		<SectionHeader
			title="Security Training Modules"
			subtitle="Interactive lessons on common cybersecurity threats and defenses. Each module includes hands-on demos to help you understand vulnerabilities and how to prevent them."
		/>
	</header>

	<!-- Filters -->
	<div class="flex items-center gap-2 mb-6">
		<span class="text-sm text-text-muted">Filter by difficulty:</span>
		{#each ['All', 'Beginner', 'Intermediate', 'Advanced'] as diff}
			<button
				class={cn(
					"px-3 py-1.5 text-sm rounded-lg transition-colors",
					selectedDifficulty === diff
						? "bg-brand text-white"
						: "bg-muted text-text-muted hover:text-text"
				)}
				onclick={() => selectedDifficulty = diff as typeof selectedDifficulty}
			>
				{diff}
			</button>
		{/each}
	</div>

	<!-- Module Grid -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
		{#each filteredModules as module}
			<a 
				href={module.href}
				class={cn(
					uiTokens.cardHover,
					"block p-6 group"
				)}
			>
				<div class="flex items-start gap-4 mb-4">
					<div class="size-12 rounded-xl bg-brand-soft flex items-center justify-center text-2xl shrink-0 group-hover:scale-110 transition-transform">
						{module.icon}
					</div>
					<div class="flex-1 min-w-0">
						<div class="flex items-center gap-2 mb-1">
							<h3 class="font-semibold text-text truncate">{module.title}</h3>
						</div>
						<Badge variant={difficultyColors[module.difficulty]} className="text-xs">
							{module.difficulty}
						</Badge>
					</div>
				</div>
				
				<p class="text-sm text-text-muted mb-4 line-clamp-2">{module.description}</p>
				
				<div class="flex flex-wrap gap-1.5 mb-4">
					{#each module.topics.slice(0, 3) as topic}
						<span class="px-2 py-0.5 text-xs rounded-full bg-muted text-text-muted">{topic}</span>
					{/each}
					{#if module.topics.length > 3}
						<span class="px-2 py-0.5 text-xs rounded-full bg-muted text-text-muted">+{module.topics.length - 3}</span>
					{/if}
				</div>
				
				<div class="flex items-center justify-between text-sm">
					<span class="flex items-center gap-1.5 text-text-muted">
						<svg class="size-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
						{module.estimatedTime}
					</span>
					<span class="text-brand font-medium group-hover:underline">
						Start Learning
						<svg class="inline size-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
						</svg>
					</span>
				</div>
				
				{#if module.progress !== undefined && module.progress > 0}
					<div class="mt-4 pt-4 border-t border-border">
						<div class="flex items-center justify-between text-xs mb-1.5">
							<span class="text-text-muted">Progress</span>
							<span class="text-text">{module.progress}%</span>
						</div>
						<ProgressBar value={module.progress} max={100} size="sm" />
					</div>
				{/if}
			</a>
		{/each}
	</div>

	<!-- Coming Soon Section -->
	<section class="mt-12">
		<h2 class="text-lg font-semibold text-text mb-4">Coming Soon</h2>
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
			{#each [
				{ title: 'Social Engineering', icon: '🎭', description: 'Psychological manipulation techniques' },
				{ title: 'Network Security', icon: '🌐', description: 'Firewalls, VPNs, and network attacks' },
				{ title: 'Cryptography Basics', icon: '🔑', description: 'Encryption, hashing, and digital signatures' }
			] as coming}
				<div class={cn(uiTokens.cardMuted, "p-5 opacity-60")}>
					<div class="flex items-center gap-3 mb-2">
						<span class="text-xl">{coming.icon}</span>
						<h3 class="font-medium text-text">{coming.title}</h3>
					</div>
					<p class="text-sm text-text-muted">{coming.description}</p>
					<Badge variant="neutral" className="mt-3">Coming Soon</Badge>
				</div>
			{/each}
		</div>
	</section>
</div>
