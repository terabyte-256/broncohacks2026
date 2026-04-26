<script lang="ts">
	import { ModuleLayout, CodeEditor, DemoSandbox, AttackVisualizer } from '$lib/components/demo';
	import { Card, Button, Alert, Badge } from '$lib/components';
	import { cn, uiTokens } from '$lib/theme';

	// Vulnerable code example
	let userInput = $state('<img src=x onerror="alert(\'XSS!\')">');
	
	// Safe vs vulnerable toggle
	let isSafeMode = $state(false);

	// Demo state
	let demoStep = $state(-1);
	let alertTriggered = $state(false);

	const vulnerableCode = `<!-- Vulnerable Code -->
<div id="greeting"></div>

<script>
  // User input inserted directly - DANGEROUS!
  const name = getUserInput();
  document.getElementById('greeting').innerHTML = 
    'Hello, ' + name;
<\/script>`;

	const safeCode = `<!-- Safe Code -->
<div id="greeting"></div>

<script>
  // User input properly escaped - SAFE!
  const name = getUserInput();
  document.getElementById('greeting').textContent = 
    'Hello, ' + name;
<\/script>`;

	const attackSteps = [
		{ icon: '👤', label: 'Attacker', description: 'Crafts malicious input with script' },
		{ icon: '📝', label: 'Input', description: 'Submits payload via form/URL' },
		{ icon: '🖥️', label: 'Server', description: 'Stores/reflects unsanitized data' },
		{ icon: '👁️', label: 'Victim', description: 'Views page with injected script' },
		{ icon: '⚡', label: 'Execute', description: 'Script runs in victim\'s browser' }
	];

	function generatePreviewHtml(input: string, safe: boolean): string {
		if (safe) {
			// Escape HTML entities
			const escaped = input
				.replace(/&/g, '&amp;')
				.replace(/</g, '&lt;')
				.replace(/>/g, '&gt;')
				.replace(/"/g, '&quot;')
				.replace(/'/g, '&#x27;');
			return `
				<h3>Comment Section</h3>
				<div class="comment">User says: ${escaped}</div>
			`;
		}
		return `
			<h3>Comment Section</h3>
			<div class="comment">User says: ${input}</div>
		`;
	}

	function runDemo() {
		demoStep = 0;
		const interval = setInterval(() => {
			demoStep++;
			if (demoStep >= attackSteps.length - 1) {
				clearInterval(interval);
			}
		}, 1000);
	}

	function handleAlert(msg: string) {
		alertTriggered = true;
	}
</script>

<ModuleLayout
	title="Cross-Site Scripting (XSS)"
	subtitle="Learn how attackers inject malicious scripts into web pages and how to prevent it"
	icon="💉"
	difficulty="Beginner"
	estimatedTime="15 min"
	track="developer"
>
	<!-- What is XSS -->
	<section>
		<Card title="What is XSS?">
			<p class="text-text-muted leading-relaxed">
				Cross-Site Scripting (XSS) is a security vulnerability that allows attackers to inject malicious scripts into web pages viewed by other users. When a victim visits the compromised page, the injected script executes in their browser with full access to cookies, session tokens, and sensitive data.
			</p>
			
			<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
				<div class="p-4 rounded-lg bg-muted">
					<h4 class="font-semibold text-text mb-2">Reflected XSS</h4>
					<p class="text-sm text-text-muted">Payload is reflected off the server in error messages, search results, or any response that includes user input.</p>
				</div>
				<div class="p-4 rounded-lg bg-muted">
					<h4 class="font-semibold text-text mb-2">Stored XSS</h4>
					<p class="text-sm text-text-muted">Malicious script is permanently stored on the target server, like in a database, message forum, or comment field.</p>
				</div>
				<div class="p-4 rounded-lg bg-muted">
					<h4 class="font-semibold text-text mb-2">DOM-based XSS</h4>
					<p class="text-sm text-text-muted">Vulnerability exists in client-side code rather than server-side code, modifying the DOM environment.</p>
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
						<h3 class="text-base font-semibold text-text">How XSS Attacks Work</h3>
						<p class="mt-1 text-sm text-text-muted">Watch the attack flow step by step</p>
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
						<p class="mt-1 text-sm text-text-muted">Try injecting a script and see what happens</p>
					</div>
					<div class="flex items-center gap-3">
						<span class="text-sm text-text-muted">Safe Mode:</span>
						<button 
							class={cn(
								"relative w-12 h-6 rounded-full transition-colors",
								isSafeMode ? "bg-success" : "bg-danger"
							)}
							onclick={() => { isSafeMode = !isSafeMode; alertTriggered = false; }}
							aria-label="Toggle safe mode"
						>
							<span class={cn(
								"absolute top-1 size-4 rounded-full bg-white transition-transform",
								isSafeMode ? "translate-x-7" : "translate-x-1"
							)}></span>
						</button>
					</div>
				</div>
			{/snippet}
			
			{#if alertTriggered && !isSafeMode}
				<Alert variant="danger" className="mb-4">
					<strong>XSS Attack Successful!</strong> The script executed in the sandbox. In a real application, this could steal cookies, hijack sessions, or perform actions as the user.
				</Alert>
			{/if}
			
			{#if isSafeMode}
				<Alert variant="success" className="mb-4">
					<strong>Safe Mode Active!</strong> User input is properly escaped, preventing script execution.
				</Alert>
			{/if}
			
			<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
				<div>
					<label class="block text-sm font-medium text-text mb-2">
						Your Input (try the XSS payload)
					</label>
					<CodeEditor
						bind:code={userInput}
						language="html"
						title="User Input"
					/>
					
					<div class="mt-3 space-y-2">
						<p class="text-xs text-text-muted">Try these payloads:</p>
						<div class="flex flex-wrap gap-2">
							<button 
								class="px-2 py-1 text-xs rounded bg-muted hover:bg-border text-text-muted transition-colors"
								onclick={() => userInput = '<script>alert("XSS!")<\/script>'}
							>
								Basic Script
							</button>
							<button 
								class="px-2 py-1 text-xs rounded bg-muted hover:bg-border text-text-muted transition-colors"
								onclick={() => userInput = '<img src=x onerror="alert(\'XSS!\')">'}
							>
								IMG Onerror
							</button>
							<button 
								class="px-2 py-1 text-xs rounded bg-muted hover:bg-border text-text-muted transition-colors"
								onclick={() => userInput = '<svg onload="alert(\'XSS!\')">'}
							>
								SVG Onload
							</button>
						</div>
					</div>
				</div>
				
				<DemoSandbox
					html={generatePreviewHtml(userInput, isSafeMode)}
					title={isSafeMode ? "Preview (Safe)" : "Preview (Vulnerable)"}
					onAlert={handleAlert}
				/>
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
						<span class="text-sm text-text-muted">Using innerHTML</span>
					</div>
					<CodeEditor code={vulnerableCode} language="html" readonly />
				</div>
				<div>
					<div class="flex items-center gap-2 mb-2">
						<Badge variant="success">Safe</Badge>
						<span class="text-sm text-text-muted">Using textContent</span>
					</div>
					<CodeEditor code={safeCode} language="html" readonly />
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
						<h4 class="font-semibold text-text">Output Encoding</h4>
						<p class="text-sm text-text-muted mt-1">Always encode user input before rendering. Use <code class="px-1 py-0.5 bg-canvas rounded text-brand">textContent</code> instead of <code class="px-1 py-0.5 bg-canvas rounded text-danger">innerHTML</code>.</p>
					</div>
				</div>
				
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">Content Security Policy (CSP)</h4>
						<p class="text-sm text-text-muted mt-1">Implement CSP headers to restrict which scripts can execute. This provides defense-in-depth even if XSS vulnerabilities exist.</p>
					</div>
				</div>
				
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">Input Validation</h4>
						<p class="text-sm text-text-muted mt-1">Validate and sanitize all user input on both client and server side. Use allowlists rather than blocklists.</p>
					</div>
				</div>
				
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">HTTPOnly Cookies</h4>
						<p class="text-sm text-text-muted mt-1">Set the HTTPOnly flag on sensitive cookies to prevent JavaScript access, limiting the damage of XSS attacks.</p>
					</div>
				</div>
			</div>
		</Card>
	</section>
</ModuleLayout>
