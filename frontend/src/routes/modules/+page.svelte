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
		available: boolean;
	}

	interface Track {
		id: string;
		title: string;
		description: string;
		icon: string;
		color: string;
		modules: Module[];
	}

	const tracks: Track[] = [
		{
			id: 'everyday',
			title: 'Everyday Security',
			description: 'Essential security skills for everyone. No technical background required.',
			icon: '🛡️',
			color: 'success',
			modules: [
				{
					id: 'phishing',
					title: 'Phishing Attacks',
					description: 'Learn to identify and protect yourself from social engineering attacks via email, SMS, and other channels.',
					icon: '🎣',
					difficulty: 'Beginner',
					estimatedTime: '15 min',
					topics: ['Email phishing', 'Spear phishing', 'Red flags', 'Verification'],
					href: '/modules/phishing',
					available: true
				},
				{
					id: 'password-security',
					title: 'Password Security',
					description: 'Understand how passwords are attacked and learn to create strong, secure passwords using best practices.',
					icon: '🔐',
					difficulty: 'Beginner',
					estimatedTime: '15 min',
					topics: ['Brute force', 'Dictionary attacks', 'Password managers', '2FA'],
					href: '/modules/password-security',
					available: true
				},
				{
					id: 'social-engineering',
					title: 'Social Engineering',
					description: 'Recognize psychological manipulation tactics used by attackers to gain unauthorized access.',
					icon: '🎭',
					difficulty: 'Beginner',
					estimatedTime: '20 min',
					topics: ['Pretexting', 'Baiting', 'Tailgating', 'Quid pro quo'],
					href: '/modules/social-engineering',
					available: false
				},
				{
					id: 'safe-browsing',
					title: 'Safe Browsing',
					description: 'Learn to identify malicious websites, avoid malware, and browse the internet safely.',
					icon: '🌐',
					difficulty: 'Beginner',
					estimatedTime: '15 min',
					topics: ['HTTPS', 'Malicious downloads', 'Browser security', 'Ad blockers'],
					href: '/modules/safe-browsing',
					available: false
				}
			]
		},
		{
			id: 'developer',
			title: 'Developer Security',
			description: 'Security fundamentals for building secure web applications.',
			icon: '👨‍💻',
			color: 'brand',
			modules: [
				{
					id: 'xss',
					title: 'Cross-Site Scripting (XSS)',
					description: 'Learn how attackers inject malicious scripts into web pages and how to prevent it with proper output encoding and CSP.',
					icon: '💉',
					difficulty: 'Beginner',
					estimatedTime: '15 min',
					topics: ['Reflected XSS', 'Stored XSS', 'DOM-based XSS', 'Defense strategies'],
					href: '/modules/xss',
					available: true
				},
				{
					id: 'sql-injection',
					title: 'SQL Injection',
					description: 'Understand how attackers manipulate database queries to access unauthorized data and how to use parameterized queries.',
					icon: '🗄️',
					difficulty: 'Intermediate',
					estimatedTime: '20 min',
					topics: ['In-band SQLi', 'Blind SQLi', 'Parameterized queries', 'ORM usage'],
					href: '/modules/sql-injection',
					available: true
				},
				{
					id: 'csrf',
					title: 'Cross-Site Request Forgery',
					description: 'Discover how attackers trick users into performing unwanted actions and how CSRF tokens protect against these attacks.',
					icon: '🎯',
					difficulty: 'Intermediate',
					estimatedTime: '15 min',
					topics: ['CSRF attacks', 'Token validation', 'SameSite cookies', 'Origin headers'],
					href: '/modules/csrf',
					available: true
				},
				{
					id: 'auth-security',
					title: 'Authentication Security',
					description: 'Build secure authentication flows with proper session management, JWT handling, and OAuth best practices.',
					icon: '🔑',
					difficulty: 'Intermediate',
					estimatedTime: '25 min',
					topics: ['Session management', 'JWT security', 'OAuth flows', 'MFA implementation'],
					href: '/modules/auth-security',
					available: false
				},
				{
					id: 'api-security',
					title: 'API Security',
					description: 'Secure your APIs with proper authentication, rate limiting, input validation, and CORS configuration.',
					icon: '🔌',
					difficulty: 'Advanced',
					estimatedTime: '25 min',
					topics: ['Rate limiting', 'Input validation', 'CORS', 'API keys'],
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

	const trackColors = {
		'success': 'border-success-border bg-success-soft',
		'brand': 'border-brand-border bg-brand-soft'
	} as const;

	let selectedTrack = $state<'all' | 'everyday' | 'developer'>('all');
	let selectedDifficulty = $state<'All' | 'Beginner' | 'Intermediate' | 'Advanced'>('All');

	const filteredTracks = $derived(() => {
		if (selectedTrack === 'all') return tracks;
		return tracks.filter(t => t.id === selectedTrack);
	});

	function filterModules(modules: Module[]) {
		if (selectedDifficulty === 'All') return modules;
		return modules.filter(m => m.difficulty === selectedDifficulty);
	}

	const totalModules = tracks.reduce((sum, t) => sum + t.modules.length, 0);
	const availableModules = tracks.reduce((sum, t) => sum + t.modules.filter(m => m.available).length, 0);
</script>

<svelte:head>
	<title>Security Modules | CyberLearn</title>
	<meta name="description" content="Interactive cybersecurity training modules organized by learning track. Master everyday security and developer security skills." />
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
			subtitle="Interactive lessons organized into learning tracks. Each module includes hands-on demos to help you understand vulnerabilities and how to prevent them."
		/>

		<!-- Stats -->
		<div class="flex items-center gap-4 mt-4 text-sm text-text-muted">
			<span class="flex items-center gap-1.5">
				<svg class="size-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
				</svg>
				{tracks.length} Learning Tracks
			</span>
			<span class="flex items-center gap-1.5">
				<svg class="size-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
				</svg>
				{availableModules} of {totalModules} Modules Available
			</span>
		</div>
	</header>

	<!-- Filters -->
	<div class="flex flex-wrap items-center gap-4 mb-8 p-4 rounded-xl bg-muted border border-border">
		<div class="flex items-center gap-2">
			<span class="text-sm font-medium text-text">Track:</span>
			{#each [{ id: 'all', label: 'All Tracks' }, { id: 'everyday', label: 'Everyday Security' }, { id: 'developer', label: 'Developer Security' }] as track}
				<button
					class={cn(
						"px-3 py-1.5 text-sm rounded-lg transition-colors",
						selectedTrack === track.id
							? "bg-brand text-white"
							: "bg-surface text-text-muted hover:text-text border border-border"
					)}
					onclick={() => selectedTrack = track.id as typeof selectedTrack}
				>
					{track.label}
				</button>
			{/each}
		</div>
		
		<div class="h-6 w-px bg-border hidden sm:block"></div>
		
		<div class="flex items-center gap-2">
			<span class="text-sm font-medium text-text">Difficulty:</span>
			{#each ['All', 'Beginner', 'Intermediate', 'Advanced'] as diff}
				<button
					class={cn(
						"px-3 py-1.5 text-sm rounded-lg transition-colors",
						selectedDifficulty === diff
							? "bg-brand text-white"
							: "bg-surface text-text-muted hover:text-text border border-border"
					)}
					onclick={() => selectedDifficulty = diff as typeof selectedDifficulty}
				>
					{diff}
				</button>
			{/each}
		</div>
	</div>

	<!-- Tracks -->
	<div class="space-y-12">
		{#each filteredTracks() as track}
			{@const trackModules = filterModules(track.modules)}
			{#if trackModules.length > 0}
				<section>
					<!-- Track Header -->
					<div class={cn("flex items-start gap-4 p-5 rounded-xl mb-6 border", trackColors[track.color as keyof typeof trackColors])}>
						<div class="size-14 rounded-xl bg-surface flex items-center justify-center text-3xl shrink-0 shadow-sm">
							{track.icon}
						</div>
						<div class="flex-1">
							<h2 class="text-xl font-bold text-text mb-1">{track.title}</h2>
							<p class="text-sm text-text-muted">{track.description}</p>
							<div class="flex items-center gap-4 mt-2 text-xs text-text-muted">
								<span>{track.modules.filter(m => m.available).length} of {track.modules.length} modules available</span>
								<span class="flex items-center gap-1">
									<svg class="size-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
									</svg>
									~{track.modules.reduce((sum, m) => sum + parseInt(m.estimatedTime), 0)} min total
								</span>
							</div>
						</div>
					</div>

					<!-- Module Grid -->
					<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
						{#each trackModules as module}
							{#if module.available}
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
											<h3 class="font-semibold text-text mb-1">{module.title}</h3>
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
							{:else}
								<!-- Coming Soon Module -->
								<div class={cn(uiTokens.cardMuted, "p-6 opacity-60")}>
									<div class="flex items-start gap-4 mb-4">
										<div class="size-12 rounded-xl bg-muted flex items-center justify-center text-2xl shrink-0">
											{module.icon}
										</div>
										<div class="flex-1 min-w-0">
											<h3 class="font-semibold text-text mb-1">{module.title}</h3>
											<Badge variant="neutral" className="text-xs">Coming Soon</Badge>
										</div>
									</div>
									<p class="text-sm text-text-muted mb-4 line-clamp-2">{module.description}</p>
									<div class="flex flex-wrap gap-1.5">
										{#each module.topics.slice(0, 2) as topic}
											<span class="px-2 py-0.5 text-xs rounded-full bg-surface text-text-muted">{topic}</span>
										{/each}
									</div>
								</div>
							{/if}
						{/each}
					</div>
				</section>
			{/if}
		{/each}
	</div>

	<!-- Empty State -->
	{#if filteredTracks().every(t => filterModules(t.modules).length === 0)}
		<div class="text-center py-12">
			<div class="size-16 rounded-full bg-muted flex items-center justify-center mx-auto mb-4">
				<svg class="size-8 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
			</div>
			<h3 class="text-lg font-semibold text-text mb-2">No modules found</h3>
			<p class="text-text-muted mb-4">Try adjusting your filters to see more modules.</p>
			<Button variant="secondary" onclick={() => { selectedTrack = 'all'; selectedDifficulty = 'All'; }}>
				Clear Filters
			</Button>
		</div>
	{/if}
</div>
