<script lang="ts">
	import { ModuleLayout, CodeEditor, AttackVisualizer } from '$lib/components/demo';
	import { Card, Button, Alert, Badge } from '$lib/components';
	import { cn, uiTokens } from '$lib/theme';

	// Demo state
	let demoStep = $state(-1);
	let attackSimulated = $state(false);
	let hasCSRFToken = $state(false);
	let bankBalance = $state(10000);
	let transferLog = $state<string[]>([]);

	const attackSteps = [
		{ icon: '🎭', label: 'Attacker', description: 'Creates malicious website' },
		{ icon: '📧', label: 'Lure', description: 'Sends link to victim' },
		{ icon: '👁️', label: 'Visit', description: 'Victim visits malicious site' },
		{ icon: '📤', label: 'Request', description: 'Hidden form auto-submits' },
		{ icon: '💸', label: 'Transfer', description: 'Bank processes request!' }
	];

	const maliciousPageCode = `<!-- Attacker's malicious page -->
<html>
<body>
  <h1>You won a prize! 🎉</h1>
  
  <!-- Hidden form that auto-submits -->
  <form action="https://bank.com/transfer" 
        method="POST" id="evil-form">
    <input type="hidden" name="to" value="attacker" />
    <input type="hidden" name="amount" value="1000" />
  </form>
  
  <script>
    // Auto-submit when page loads
    document.getElementById('evil-form').submit();
  <\/script>
</body>
</html>`;

	const vulnerableServerCode = `// VULNERABLE - No CSRF protection
app.post('/transfer', (req, res) => {
  const { to, amount } = req.body;
  
  // Only checks session cookie (auto-sent!)
  if (req.session.user) {
    transferMoney(req.session.user, to, amount);
    res.json({ success: true });
  }
});`;

	const safeServerCode = `// SAFE - CSRF token validation
app.post('/transfer', (req, res) => {
  const { to, amount, csrfToken } = req.body;
  
  // Verify CSRF token matches session
  if (!validateCSRFToken(req.session, csrfToken)) {
    return res.status(403).json({ 
      error: 'Invalid CSRF token' 
    });
  }
  
  if (req.session.user) {
    transferMoney(req.session.user, to, amount);
    res.json({ success: true });
  }
});`;

	function runDemo() {
		demoStep = 0;
		const interval = setInterval(() => {
			demoStep++;
			if (demoStep >= attackSteps.length - 1) {
				clearInterval(interval);
			}
		}, 1000);
	}

	function simulateAttack() {
		if (hasCSRFToken) {
			transferLog = [...transferLog, '❌ Transfer BLOCKED - Invalid CSRF token'];
		} else {
			bankBalance -= 1000;
			transferLog = [...transferLog, '⚠️ $1,000 transferred to attacker!'];
			attackSimulated = true;
		}
	}

	function resetDemo() {
		bankBalance = 10000;
		transferLog = [];
		attackSimulated = false;
	}
</script>

<ModuleLayout
	title="Cross-Site Request Forgery (CSRF)"
	subtitle="Learn how attackers trick users into performing unwanted actions on authenticated sites"
	icon="🎯"
	difficulty="Intermediate"
	estimatedTime="15 min"
	track="developer"
>
	<!-- What is CSRF -->
	<section>
		<Card title="What is CSRF?">
			<p class="text-text-muted leading-relaxed">
				Cross-Site Request Forgery (CSRF) is an attack that tricks authenticated users into submitting unwanted requests. Unlike XSS which exploits user trust in a website, CSRF exploits a website&apos;s trust in the user&apos;s browser. The attack works because browsers automatically include cookies with every request to a domain.
			</p>
			
			<div class="mt-6 p-4 rounded-lg bg-danger-soft border border-danger-border">
				<h4 class="font-semibold text-danger mb-2">Real-World Impact</h4>
				<p class="text-sm text-danger">
					CSRF attacks can result in unauthorized fund transfers, email address changes, password resets, or any action the victim is authorized to perform. In 2008, a CSRF vulnerability in uTorrent allowed attackers to download malicious torrents without user consent.
				</p>
			</div>
		</Card>
	</section>

	<!-- Attack Flow Visualization -->
	<section>
		<Card>
			{#snippet header()}
				<div class="flex items-center justify-between">
					<div>
						<h3 class="text-base font-semibold text-text">How CSRF Attacks Work</h3>
						<p class="mt-1 text-sm text-text-muted">The anatomy of a CSRF attack</p>
					</div>
					<Button size="sm" onclick={runDemo}>
						{demoStep >= 0 ? 'Replay' : 'Start Demo'}
					</Button>
				</div>
			{/snippet}
			
			<AttackVisualizer steps={attackSteps} currentStep={demoStep} />
		</Card>
	</section>

	<!-- Interactive Demo -->
	<section>
		<Card>
			{#snippet header()}
				<div class="flex items-center justify-between">
					<div>
						<h3 class="text-base font-semibold text-text">Interactive Demo</h3>
						<p class="mt-1 text-sm text-text-muted">Simulate a CSRF attack on a banking application</p>
					</div>
					<div class="flex items-center gap-3">
						<span class="text-sm text-text-muted">CSRF Protection:</span>
						<button 
							class={cn(
								"relative w-12 h-6 rounded-full transition-colors",
								hasCSRFToken ? "bg-success" : "bg-danger"
							)}
							onclick={() => { hasCSRFToken = !hasCSRFToken; }}
							aria-label="Toggle CSRF protection"
						>
							<span class={cn(
								"absolute top-1 size-4 rounded-full bg-white transition-transform",
								hasCSRFToken ? "translate-x-7" : "translate-x-1"
							)}></span>
						</button>
					</div>
				</div>
			{/snippet}
			
			{#if hasCSRFToken}
				<Alert variant="success" className="mb-4">
					<strong>CSRF Protection Active!</strong> All forms require valid CSRF tokens.
				</Alert>
			{:else}
				<Alert variant="warning" className="mb-4">
					<strong>No CSRF Protection!</strong> The bank accepts any request with valid session cookies.
				</Alert>
			{/if}
			
			<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<!-- Bank Dashboard Simulation -->
				<div class="space-y-4">
					<div class="p-4 rounded-lg bg-muted border border-border">
						<div class="flex items-center gap-2 mb-3">
							<span class="text-lg">🏦</span>
							<h4 class="font-semibold text-text">SecureBank Dashboard</h4>
						</div>
						<div class="p-3 rounded bg-canvas">
							<p class="text-sm text-text-muted">Account Balance</p>
							<p class="text-2xl font-bold text-text">${bankBalance.toLocaleString()}</p>
						</div>
						<p class="text-xs text-text-muted mt-2">You are logged in as: user@example.com</p>
					</div>
					
					<!-- Malicious Page Simulation -->
					<div class="p-4 rounded-lg bg-danger-soft border border-danger-border">
						<div class="flex items-center gap-2 mb-3">
							<span class="text-lg">⚠️</span>
							<h4 class="font-semibold text-danger">Malicious Website</h4>
						</div>
						<p class="text-sm text-text mb-3">You received an email: &quot;Click here to claim your prize!&quot;</p>
						<Button variant="danger" onclick={simulateAttack}>
							Visit Malicious Site
						</Button>
					</div>

					<!-- Transfer Log -->
					{#if transferLog.length > 0}
						<div class="p-4 rounded-lg bg-canvas border border-border">
							<h4 class="font-medium text-text mb-2">Activity Log</h4>
							<div class="space-y-1">
								{#each transferLog as log}
									<p class="text-sm {log.startsWith('❌') ? 'text-success' : 'text-danger'}">{log}</p>
								{/each}
							</div>
							<Button variant="ghost" size="sm" onclick={resetDemo} className="mt-3">
								Reset Demo
							</Button>
						</div>
					{/if}
				</div>

				<!-- Malicious Page Code -->
				<div class="space-y-4">
					<h4 class="font-medium text-text">Attacker&apos;s Malicious Page</h4>
					<CodeEditor code={maliciousPageCode} language="html" readonly title="evil-page.html" />
					<p class="text-sm text-text-muted">
						When the victim visits this page, the hidden form automatically submits a transfer request to the bank. Since the victim is logged in, their session cookie is sent automatically!
					</p>
				</div>
			</div>
		</Card>
	</section>

	<!-- Code Comparison -->
	<section>
		<Card title="Vulnerable vs Safe Code">
			<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
				<div>
					<div class="flex items-center gap-2 mb-2">
						<Badge variant="danger">Vulnerable</Badge>
						<span class="text-sm text-text-muted">No CSRF validation</span>
					</div>
					<CodeEditor code={vulnerableServerCode} language="javascript" readonly />
				</div>
				<div>
					<div class="flex items-center gap-2 mb-2">
						<Badge variant="success">Safe</Badge>
						<span class="text-sm text-text-muted">CSRF token required</span>
					</div>
					<CodeEditor code={safeServerCode} language="javascript" readonly />
				</div>
			</div>
		</Card>
	</section>

	<!-- Defense Strategies -->
	<section>
		<Card title="Defense Strategies">
			<div class="space-y-4">
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">CSRF Tokens</h4>
						<p class="text-sm text-text-muted mt-1">Include a unique, unpredictable token in each form. The server validates this token with each request. Attackers can&apos;t forge the token because they can&apos;t read it from another domain.</p>
					</div>
				</div>
				
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">SameSite Cookies</h4>
						<p class="text-sm text-text-muted mt-1">Set cookies with <code class="px-1 py-0.5 bg-canvas rounded text-brand">SameSite=Strict</code> or <code class="px-1 py-0.5 bg-canvas rounded text-brand">SameSite=Lax</code> to prevent them from being sent with cross-origin requests.</p>
					</div>
				</div>
				
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">Origin/Referer Validation</h4>
						<p class="text-sm text-text-muted mt-1">Check the Origin or Referer header to verify requests come from your domain. This is a defense-in-depth measure.</p>
					</div>
				</div>
				
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">Re-authentication</h4>
						<p class="text-sm text-text-muted mt-1">Require password confirmation or 2FA for sensitive operations like changing email, password, or transferring funds.</p>
					</div>
				</div>
			</div>
		</Card>
	</section>
</ModuleLayout>
