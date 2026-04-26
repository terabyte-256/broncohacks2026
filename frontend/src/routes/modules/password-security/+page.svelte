<script lang="ts">
	import { ModuleLayout, CodeEditor, AttackVisualizer } from '$lib/components/demo';
	import { Card, Button, Alert, Badge, Input, ProgressBar } from '$lib/components';
	import { cn, uiTokens } from '$lib/theme';

	// Demo state
	let password = $state('');
	let showPassword = $state(false);
	let crackingDemo = $state(false);
	let crackedPasswords = $state<string[]>([]);
	let demoStep = $state(-1);

	const attackSteps = [
		{ icon: '📋', label: 'Breach', description: 'Database is compromised' },
		{ icon: '🔐', label: 'Hashes', description: 'Password hashes obtained' },
		{ icon: '💻', label: 'Crack', description: 'Offline cracking begins' },
		{ icon: '📖', label: 'Dictionary', description: 'Common passwords tried' },
		{ icon: '🔓', label: 'Success', description: 'Weak passwords cracked!' }
	];

	// Password strength calculation
	function calculateStrength(pwd: string): { score: number; level: string; feedback: string[]; crackTime: string } {
		if (!pwd) return { score: 0, level: 'None', feedback: [], crackTime: 'N/A' };

		let score = 0;
		const feedback: string[] = [];

		// Length checks
		if (pwd.length >= 8) score += 20;
		else feedback.push('Use at least 8 characters');
		
		if (pwd.length >= 12) score += 15;
		else if (pwd.length >= 8) feedback.push('Consider using 12+ characters');
		
		if (pwd.length >= 16) score += 10;

		// Character variety
		if (/[a-z]/.test(pwd)) score += 10;
		else feedback.push('Add lowercase letters');
		
		if (/[A-Z]/.test(pwd)) score += 10;
		else feedback.push('Add uppercase letters');
		
		if (/[0-9]/.test(pwd)) score += 10;
		else feedback.push('Add numbers');
		
		if (/[^a-zA-Z0-9]/.test(pwd)) score += 15;
		else feedback.push('Add special characters (!@#$%^&*)');

		// Penalty for common patterns
		const commonPatterns = ['password', '123456', 'qwerty', 'abc123', 'letmein', 'admin', 'welcome'];
		if (commonPatterns.some(p => pwd.toLowerCase().includes(p))) {
			score -= 30;
			feedback.push('Avoid common words and patterns');
		}

		// Penalty for repeated characters
		if (/(.)\1{2,}/.test(pwd)) {
			score -= 10;
			feedback.push('Avoid repeated characters');
		}

		score = Math.max(0, Math.min(100, score));

		let level: string;
		let crackTime: string;
		
		if (score < 25) {
			level = 'Weak';
			crackTime = 'Instantly';
		} else if (score < 50) {
			level = 'Fair';
			crackTime = 'Minutes to hours';
		} else if (score < 75) {
			level = 'Good';
			crackTime = 'Days to months';
		} else {
			level = 'Strong';
			crackTime = 'Years to centuries';
		}

		return { score, level, feedback, crackTime };
	}

	const strength = $derived(calculateStrength(password));

	// Simulated password cracking demo
	const commonPasswords = [
		{ password: '123456', time: 0.001 },
		{ password: 'password', time: 0.001 },
		{ password: 'qwerty123', time: 0.5 },
		{ password: 'letmein', time: 0.001 },
		{ password: 'dragon', time: 0.01 },
		{ password: 'baseball', time: 0.1 },
		{ password: 'iloveyou', time: 0.05 },
		{ password: 'trustno1', time: 0.5 },
		{ password: 'sunshine', time: 0.2 },
		{ password: 'princess', time: 0.3 }
	];

	async function runCrackingDemo() {
		crackingDemo = true;
		crackedPasswords = [];
		
		for (const pwd of commonPasswords) {
			await new Promise(r => setTimeout(r, 200));
			crackedPasswords = [...crackedPasswords, `${pwd.password} (cracked in ${pwd.time}s)`];
		}
		
		crackingDemo = false;
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

	const hashingCode = `// BAD - Plain text storage
db.users.insert({
  email: user.email,
  password: user.password  // NEVER do this!
});

// BAD - Simple hash (crackable)
const hash = md5(user.password);

// GOOD - Proper password hashing
import bcrypt from 'bcrypt';

const saltRounds = 12;
const hash = await bcrypt.hash(password, saltRounds);

// Verification
const isValid = await bcrypt.compare(
  inputPassword, 
  storedHash
);`;
</script>

<ModuleLayout
	title="Password Security"
	subtitle="Understand how passwords are attacked and learn to create strong, secure passwords"
	icon="🔐"
	difficulty="Beginner"
	estimatedTime="15 min"
	track="everyday"
>
	<!-- What is Password Security -->
	<section>
		<Card title="Why Password Security Matters">
			<p class="text-text-muted leading-relaxed">
				Passwords are the most common form of authentication, yet weak passwords remain one of the biggest security vulnerabilities. Attackers use various techniques to crack passwords, from simple guessing to sophisticated brute-force attacks using powerful hardware.
			</p>
			
			<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
				<div class="p-4 rounded-lg bg-muted">
					<h4 class="font-semibold text-text mb-2">Brute Force</h4>
					<p class="text-sm text-text-muted">Trying every possible combination. Short passwords fall quickly to this attack.</p>
				</div>
				<div class="p-4 rounded-lg bg-muted">
					<h4 class="font-semibold text-text mb-2">Dictionary Attack</h4>
					<p class="text-sm text-text-muted">Using lists of common passwords and words. Most leaked passwords are dictionary words.</p>
				</div>
				<div class="p-4 rounded-lg bg-muted">
					<h4 class="font-semibold text-text mb-2">Credential Stuffing</h4>
					<p class="text-sm text-text-muted">Using leaked credentials from other breaches. Password reuse makes this devastating.</p>
				</div>
			</div>

			<div class="mt-6 p-4 rounded-lg bg-danger-soft border border-danger-border">
				<h4 class="font-semibold text-danger mb-2">Shocking Statistics</h4>
				<p class="text-sm text-danger">
					Over 80% of data breaches involve weak or stolen passwords. The password &quot;123456&quot; has been found in over 23 million breached accounts. Modern GPUs can test billions of password combinations per second.
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
						<h3 class="text-base font-semibold text-text">How Password Attacks Work</h3>
						<p class="mt-1 text-sm text-text-muted">From breach to cracked passwords</p>
					</div>
					<Button size="sm" onclick={runDemo}>
						{demoStep >= 0 ? 'Replay' : 'Start Demo'}
					</Button>
				</div>
			{/snippet}
			
			<AttackVisualizer steps={attackSteps} currentStep={demoStep} />
		</Card>
	</section>

	<!-- Password Strength Checker -->
	<section>
		<Card>
			{#snippet header()}
				<div>
					<h3 class="text-base font-semibold text-text">Password Strength Analyzer</h3>
					<p class="mt-1 text-sm text-text-muted">Test how strong your password would be</p>
				</div>
			{/snippet}
			
			<div class="space-y-4">
				<div class="relative">
					<Input 
						type={showPassword ? 'text' : 'password'}
						bind:value={password}
						placeholder="Enter a test password..."
						size="lg"
						className="pr-14"
					/>
					<button
						type="button"
						class="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted hover:text-text transition-colors"
						onclick={() => showPassword = !showPassword}
					>
						{#if showPassword}
							<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
							</svg>
						{:else}
							<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
							</svg>
						{/if}
					</button>
				</div>

				{#if password}
					<div class="space-y-3">
						<div class="flex items-center justify-between">
							<span class="text-sm font-medium text-text">Strength: {strength.level}</span>
							<span class="text-sm text-text-muted">Time to crack: {strength.crackTime}</span>
						</div>
						
						<div class="h-2 rounded-full bg-muted overflow-hidden">
							<div 
								class={cn(
									"h-full transition-all duration-300 rounded-full",
									strength.score < 25 ? "bg-danger" :
									strength.score < 50 ? "bg-warning" :
									strength.score < 75 ? "bg-brand" : "bg-success"
								)}
								style="width: {strength.score}%"
							></div>
						</div>

						{#if strength.feedback.length > 0}
							<div class="p-3 rounded-lg bg-muted">
								<p class="text-sm font-medium text-text mb-2">Suggestions:</p>
								<ul class="space-y-1">
									{#each strength.feedback as item}
										<li class="text-sm text-text-muted flex items-center gap-2">
											<span class="text-warning">&#x2022;</span>
											{item}
										</li>
									{/each}
								</ul>
							</div>
						{:else}
							<Alert variant="success">
								Great password! It meets all security recommendations.
							</Alert>
						{/if}
					</div>
				{/if}
			</div>
		</Card>
	</section>

	<!-- Password Cracking Demo -->
	<section>
		<Card>
			{#snippet header()}
				<div class="flex items-center justify-between">
					<div>
						<h3 class="text-base font-semibold text-text">Dictionary Attack Simulation</h3>
						<p class="mt-1 text-sm text-text-muted">Watch how quickly common passwords are cracked</p>
					</div>
					<Button size="sm" onclick={runCrackingDemo} loading={crackingDemo}>
						{crackingDemo ? 'Cracking...' : 'Start Simulation'}
					</Button>
				</div>
			{/snippet}
			
			<div class="font-mono text-sm p-4 rounded-lg bg-canvas border border-border min-h-48 overflow-auto">
				{#if crackedPasswords.length === 0 && !crackingDemo}
					<p class="text-text-muted">Click &quot;Start Simulation&quot; to see dictionary attack in action...</p>
				{:else}
					<div class="space-y-1">
						<p class="text-text-muted mb-2">[*] Starting dictionary attack...</p>
						{#each crackedPasswords as pwd}
							<p class="text-danger">[!] CRACKED: {pwd}</p>
						{/each}
						{#if !crackingDemo && crackedPasswords.length > 0}
							<p class="text-warning mt-2">[*] Attack complete. 10 passwords cracked in under 3 seconds!</p>
						{/if}
					</div>
				{/if}
			</div>
		</Card>
	</section>

	<!-- Password Storage Code -->
	<section>
		<Card title="Secure Password Storage (For Developers)">
			<CodeEditor code={hashingCode} language="javascript" readonly title="password-storage.js" />
			<p class="text-sm text-text-muted mt-3">
				Never store passwords in plain text. Use bcrypt, Argon2, or scrypt with proper salt rounds. These algorithms are intentionally slow to resist brute-force attacks.
			</p>
		</Card>
	</section>

	<!-- Best Practices -->
	<section>
		<Card title="Password Best Practices">
			<div class="space-y-4">
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">Use a Password Manager</h4>
						<p class="text-sm text-text-muted mt-1">Generate and store unique, complex passwords for every account. You only need to remember one master password.</p>
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
						<p class="text-sm text-text-muted mt-1">Even if your password is compromised, 2FA provides an additional security layer. Use authenticator apps over SMS when possible.</p>
					</div>
				</div>
				
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">Use Passphrases</h4>
						<p class="text-sm text-text-muted mt-1">Consider using memorable passphrases like &quot;correct-horse-battery-staple&quot;. They&apos;re longer, easier to remember, and harder to crack.</p>
					</div>
				</div>
				
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">Never Reuse Passwords</h4>
						<p class="text-sm text-text-muted mt-1">Each account should have a unique password. When one service is breached, your other accounts remain safe.</p>
					</div>
				</div>
			</div>
		</Card>
	</section>
</ModuleLayout>
