<script lang="ts">
	import { ModuleLayout, CodeEditor, AttackVisualizer } from '$lib/components/demo';
	import { Card, Button, Alert, Badge } from '$lib/components';
	import { cn, uiTokens } from '$lib/theme';

	// Demo state
	let demoStep = $state(-1);
	let selectedEmail = $state(0);
	let showAnalysis = $state(false);
	let userGuess = $state<'phish' | 'legit' | null>(null);

	const attackSteps = [
		{ icon: '🎭', label: 'Prepare', description: 'Clone legitimate website' },
		{ icon: '📧', label: 'Craft', description: 'Create convincing email' },
		{ icon: '📤', label: 'Send', description: 'Mass distribute to targets' },
		{ icon: '🖱️', label: 'Click', description: 'Victim clicks malicious link' },
		{ icon: '🔑', label: 'Harvest', description: 'Credentials stolen!' }
	];

	const emails = [
		{
			id: 1,
			isPhish: true,
			from: 'security@paypa1.com',
			fromDisplay: 'PayPal Security Team',
			subject: 'Urgent: Your account has been limited',
			preview: 'Dear Customer, We have noticed unusual activity on your account...',
			body: `Dear Valued Customer,

We have noticed unusual activity on your PayPal account. Your account access has been limited until you verify your information.

Please click the button below to verify your account within 24 hours or your account will be permanently suspended.

[Verify My Account]

Thank you for your cooperation.

PayPal Security Team`,
			redFlags: [
				'Sender domain is "paypa1.com" (number 1 instead of letter l)',
				'Creates urgency with "24 hours" deadline',
				'Generic greeting "Dear Valued Customer"',
				'Threatens account suspension',
				'No specific account details mentioned'
			]
		},
		{
			id: 2,
			isPhish: false,
			from: 'no-reply@github.com',
			fromDisplay: 'GitHub',
			subject: 'Your two-factor authentication codes',
			preview: 'You recently requested backup codes for two-factor authentication...',
			body: `Hi @username,

You recently requested backup codes for two-factor authentication on your account.

Your new backup codes are attached to this email. Each code can only be used once.

If you didn't request these codes, please secure your account immediately by visiting:
https://github.com/settings/security

Thanks,
The GitHub Team`,
			redFlags: []
		},
		{
			id: 3,
			isPhish: true,
			from: 'admin@secure-microsoft-login.com',
			fromDisplay: 'Microsoft Account Team',
			subject: 'Re: Password Reset Confirmation',
			preview: 'Your Microsoft password was reset. If this wasn\'t you, click here...',
			body: `Your Microsoft account password was recently changed.

If you made this change, you can ignore this email.

If you DID NOT make this change, your account may be compromised. Click immediately to secure your account:

[Secure My Account Now]

Microsoft Account Team
This is an automated message.`,
			redFlags: [
				'Domain "secure-microsoft-login.com" is not microsoft.com',
				'Subject starts with "Re:" to appear like ongoing conversation',
				'Creates fear that account is compromised',
				'Urgency language: "Click immediately"',
				'Generic sign-off without specific support contact'
			]
		},
		{
			id: 4,
			isPhish: false,
			from: 'noreply@vercel.com',
			fromDisplay: 'Vercel',
			subject: 'Your deployment is live',
			preview: 'Your project my-app was successfully deployed to production...',
			body: `Your deployment is live!

Project: my-app
Deployment URL: https://my-app.vercel.app
Branch: main
Commit: feat: add new feature

View your deployment:
https://vercel.com/your-team/my-app/deployments/dpl_xxxxx

Need help? Visit our documentation or contact support.

- The Vercel Team`,
			redFlags: []
		}
	];

	const currentEmail = $derived(emails[selectedEmail]);

	function runDemo() {
		demoStep = 0;
		const interval = setInterval(() => {
			demoStep++;
			if (demoStep >= attackSteps.length - 1) {
				clearInterval(interval);
			}
		}, 1000);
	}

	function checkAnswer(guess: 'phish' | 'legit') {
		userGuess = guess;
		showAnalysis = true;
	}

	function nextEmail() {
		selectedEmail = (selectedEmail + 1) % emails.length;
		showAnalysis = false;
		userGuess = null;
	}
</script>

<ModuleLayout
	title="Phishing Attacks"
	subtitle="Learn to identify and protect yourself from social engineering attacks via email"
	icon="🎣"
	difficulty="Beginner"
	estimatedTime="15 min"
	track="everyday"
>
	<!-- What is Phishing -->
	<section>
		<Card title="What is Phishing?">
			<p class="text-text-muted leading-relaxed">
				Phishing is a social engineering attack where attackers impersonate trusted entities to trick victims into revealing sensitive information like passwords, credit card numbers, or personal data. These attacks typically arrive via email but can also occur through SMS (smishing), voice calls (vishing), or social media.
			</p>
			
			<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
				<div class="p-4 rounded-lg bg-muted">
					<h4 class="font-semibold text-text mb-2">Email Phishing</h4>
					<p class="text-sm text-text-muted">Mass emails impersonating banks, services, or colleagues. Most common type of phishing attack.</p>
				</div>
				<div class="p-4 rounded-lg bg-muted">
					<h4 class="font-semibold text-text mb-2">Spear Phishing</h4>
					<p class="text-sm text-text-muted">Targeted attacks using personal information. Often directed at specific individuals or organizations.</p>
				</div>
				<div class="p-4 rounded-lg bg-muted">
					<h4 class="font-semibold text-text mb-2">Whaling</h4>
					<p class="text-sm text-text-muted">High-value targets like executives or admins. Uses highly personalized content and urgent requests.</p>
				</div>
			</div>
		</Card>
	</section>

	<!-- Attack Flow Visualization -->
	<section>
		<Card>
			{#snippet header()}
				<div class="flex items-center justify-between">
					<div>
						<h3 class="text-base font-semibold text-text">How Phishing Attacks Work</h3>
						<p class="mt-1 text-sm text-text-muted">The typical phishing attack lifecycle</p>
					</div>
					<Button size="sm" onclick={runDemo}>
						{demoStep >= 0 ? 'Replay' : 'Start Demo'}
					</Button>
				</div>
			{/snippet}
			
			<AttackVisualizer steps={attackSteps} currentStep={demoStep} />
		</Card>
	</section>

	<!-- Interactive Demo - Spot the Phish -->
	<section>
		<Card>
			{#snippet header()}
				<div class="flex items-center justify-between">
					<div>
						<h3 class="text-base font-semibold text-text">Spot the Phish</h3>
						<p class="mt-1 text-sm text-text-muted">Can you identify which emails are phishing attempts?</p>
					</div>
					<div class="flex items-center gap-2">
						<Badge variant="neutral">Email {selectedEmail + 1} of {emails.length}</Badge>
					</div>
				</div>
			{/snippet}
			
			<!-- Email Preview -->
			<div class="rounded-lg border border-border bg-canvas overflow-hidden">
				<!-- Email Header -->
				<div class="border-b border-border p-4 space-y-2">
					<div class="flex items-center justify-between">
						<div class="flex items-center gap-3">
							<div class="size-10 rounded-full bg-muted flex items-center justify-center text-lg">
								{currentEmail.fromDisplay.charAt(0)}
							</div>
							<div>
								<p class="font-medium text-text">{currentEmail.fromDisplay}</p>
								<p class="text-sm text-text-muted">&lt;{currentEmail.from}&gt;</p>
							</div>
						</div>
					</div>
					<h4 class="font-semibold text-text">{currentEmail.subject}</h4>
				</div>
				
				<!-- Email Body -->
				<div class="p-4">
					<pre class="text-sm text-text-muted whitespace-pre-wrap font-sans leading-relaxed">{currentEmail.body}</pre>
				</div>
			</div>
			
			<!-- Answer Buttons -->
			{#if !showAnalysis}
				<div class="flex gap-4 mt-4">
					<Button variant="danger" onclick={() => checkAnswer('phish')} fullWidth>
						This is Phishing
					</Button>
					<Button variant="secondary" onclick={() => checkAnswer('legit')} fullWidth>
						This is Legitimate
					</Button>
				</div>
			{:else}
				<!-- Analysis -->
				<div class="mt-4 space-y-4">
					{#if (userGuess === 'phish') === currentEmail.isPhish}
						<Alert variant="success">
							<strong>Correct!</strong> {currentEmail.isPhish ? 'This is a phishing email.' : 'This is a legitimate email.'}
						</Alert>
					{:else}
						<Alert variant="danger">
							<strong>Incorrect!</strong> {currentEmail.isPhish ? 'This is actually a phishing email.' : 'This is actually a legitimate email.'}
						</Alert>
					{/if}
					
					{#if currentEmail.isPhish && currentEmail.redFlags.length > 0}
						<div class="p-4 rounded-lg bg-danger-soft border border-danger-border">
							<h4 class="font-semibold text-danger mb-3">Red Flags Identified:</h4>
							<ul class="space-y-2">
								{#each currentEmail.redFlags as flag}
									<li class="flex items-start gap-2 text-sm text-danger">
										<span class="mt-0.5">&#x2022;</span>
										<span>{flag}</span>
									</li>
								{/each}
							</ul>
						</div>
					{:else if !currentEmail.isPhish}
						<div class="p-4 rounded-lg bg-success-soft border border-success-border">
							<h4 class="font-semibold text-success mb-2">Why This is Legitimate:</h4>
							<ul class="space-y-2 text-sm text-success">
								<li class="flex items-start gap-2">
									<span class="mt-0.5">&#x2713;</span>
									<span>Sender email matches official domain</span>
								</li>
								<li class="flex items-start gap-2">
									<span class="mt-0.5">&#x2713;</span>
									<span>No urgency or threatening language</span>
								</li>
								<li class="flex items-start gap-2">
									<span class="mt-0.5">&#x2713;</span>
									<span>Contains specific, verifiable information</span>
								</li>
							</ul>
						</div>
					{/if}
					
					<Button onclick={nextEmail} fullWidth>
						Next Email
					</Button>
				</div>
			{/if}
		</Card>
	</section>

	<!-- Red Flags Reference -->
	<section>
		<Card title="Common Phishing Red Flags">
			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				<div class="space-y-4">
					<div class="flex gap-3 items-start">
						<span class="text-danger text-lg">1.</span>
						<div>
							<h4 class="font-semibold text-text">Suspicious Sender Address</h4>
							<p class="text-sm text-text-muted">Check the actual email address, not just display name. Look for misspellings or unusual domains.</p>
						</div>
					</div>
					<div class="flex gap-3 items-start">
						<span class="text-danger text-lg">2.</span>
						<div>
							<h4 class="font-semibold text-text">Urgency & Threats</h4>
							<p class="text-sm text-text-muted">&quot;Act now!&quot;, &quot;Your account will be closed&quot;, &quot;Immediate action required&quot;</p>
						</div>
					</div>
					<div class="flex gap-3 items-start">
						<span class="text-danger text-lg">3.</span>
						<div>
							<h4 class="font-semibold text-text">Generic Greetings</h4>
							<p class="text-sm text-text-muted">&quot;Dear Customer&quot; or &quot;Dear User&quot; instead of your actual name</p>
						</div>
					</div>
				</div>
				<div class="space-y-4">
					<div class="flex gap-3 items-start">
						<span class="text-danger text-lg">4.</span>
						<div>
							<h4 class="font-semibold text-text">Suspicious Links</h4>
							<p class="text-sm text-text-muted">Hover over links to see the real URL. Check for misspellings or unfamiliar domains.</p>
						</div>
					</div>
					<div class="flex gap-3 items-start">
						<span class="text-danger text-lg">5.</span>
						<div>
							<h4 class="font-semibold text-text">Grammar & Spelling Errors</h4>
							<p class="text-sm text-text-muted">Professional companies rarely have obvious errors in their communications.</p>
						</div>
					</div>
					<div class="flex gap-3 items-start">
						<span class="text-danger text-lg">6.</span>
						<div>
							<h4 class="font-semibold text-text">Requests for Sensitive Info</h4>
							<p class="text-sm text-text-muted">Legitimate companies rarely ask for passwords or full credit card numbers via email.</p>
						</div>
					</div>
				</div>
			</div>
		</Card>
	</section>

	<!-- Defense Strategies -->
	<section>
		<Card title="How to Protect Yourself">
			<div class="space-y-4">
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">Verify Sender Identity</h4>
						<p class="text-sm text-text-muted mt-1">Always check the actual email address, not just the display name. When in doubt, contact the company directly using contact info from their official website.</p>
					</div>
				</div>
				
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">Don&apos;t Click - Navigate Directly</h4>
						<p class="text-sm text-text-muted mt-1">Instead of clicking links in emails, type the website address directly into your browser or use your saved bookmarks.</p>
					</div>
				</div>
				
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">Enable Two-Factor Authentication</h4>
						<p class="text-sm text-text-muted mt-1">Even if attackers steal your password, 2FA provides an additional layer of protection for your accounts.</p>
					</div>
				</div>
				
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">Report Phishing Attempts</h4>
						<p class="text-sm text-text-muted mt-1">Forward suspicious emails to your IT department or the company being impersonated. Many organizations have dedicated abuse reporting addresses.</p>
					</div>
				</div>
			</div>
		</Card>
	</section>
</ModuleLayout>
