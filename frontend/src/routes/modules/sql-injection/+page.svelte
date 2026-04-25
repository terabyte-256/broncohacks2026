<script lang="ts">
	import { ModuleLayout, CodeEditor, AttackVisualizer } from '$lib/components/demo';
	import { Card, Button, Alert, Badge, Input } from '$lib/components';
	import { cn, uiTokens } from '$lib/theme';

	// Demo state
	let username = $state("admin' --");
	let password = $state("anything");
	let queryResult = $state<string | null>(null);
	let isVulnerable = $state(true);
	let demoStep = $state(-1);

	// Simulated database
	const mockUsers = [
		{ id: 1, username: 'admin', password: 'super_secret_123', role: 'admin', email: 'admin@example.com' },
		{ id: 2, username: 'john', password: 'password123', role: 'user', email: 'john@example.com' },
		{ id: 3, username: 'jane', password: 'secure456', role: 'user', email: 'jane@example.com' }
	];

	const attackSteps = [
		{ icon: '👤', label: 'Attacker', description: 'Identifies login form' },
		{ icon: '💉', label: 'Payload', description: "Crafts SQL injection: ' OR 1=1 --" },
		{ icon: '📤', label: 'Submit', description: 'Sends malicious input' },
		{ icon: '🗄️', label: 'Database', description: 'Query executes with injected SQL' },
		{ icon: '🔓', label: 'Access', description: 'Bypasses authentication!' }
	];

	function generateQuery(user: string, pass: string, safe: boolean): string {
		if (safe) {
			return `SELECT * FROM users 
WHERE username = $1 AND password = $2

-- Parameters: ['${user}', '${pass}']
-- Safely parameterized - no injection possible!`;
		}
		return `SELECT * FROM users 
WHERE username = '${user}' AND password = '${pass}'`;
	}

	function simulateQuery() {
		if (isVulnerable) {
			// Simulate vulnerable query
			if (username.includes("'") || username.includes("--") || username.includes("OR")) {
				// SQL injection detected - return all users or bypass auth
				if (username.toLowerCase().includes("or 1=1") || username.includes("' --")) {
					queryResult = JSON.stringify(mockUsers, null, 2);
				} else if (username.includes("' OR '1'='1")) {
					queryResult = JSON.stringify(mockUsers, null, 2);
				} else if (username.includes("admin' --")) {
					queryResult = JSON.stringify([mockUsers[0]], null, 2);
				} else {
					queryResult = JSON.stringify(mockUsers, null, 2);
				}
			} else {
				// Normal query
				const user = mockUsers.find(u => u.username === username && u.password === password);
				queryResult = user ? JSON.stringify([user], null, 2) : 'No results - Invalid credentials';
			}
		} else {
			// Parameterized query - safe
			const user = mockUsers.find(u => u.username === username && u.password === password);
			queryResult = user ? JSON.stringify([user], null, 2) : 'No results - Invalid credentials';
		}
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

	const vulnerableCode = `// VULNERABLE - String concatenation
const query = \`
  SELECT * FROM users 
  WHERE username = '\${username}' 
  AND password = '\${password}'
\`;

db.execute(query);`;

	const safeCode = `// SAFE - Parameterized queries
const query = \`
  SELECT * FROM users 
  WHERE username = $1 
  AND password = $2
\`;

db.execute(query, [username, password]);`;
</script>

<ModuleLayout
	title="SQL Injection"
	subtitle="Understand how attackers manipulate database queries and how to prevent data breaches"
	icon="🗄️"
	difficulty="Intermediate"
	estimatedTime="20 min"
>
	<!-- What is SQL Injection -->
	<section>
		<Card title="What is SQL Injection?">
			<p class="text-text-muted leading-relaxed">
				SQL Injection is a code injection technique that exploits vulnerabilities in applications that construct SQL queries using user input. Attackers can manipulate queries to access unauthorized data, modify database contents, or even execute administrative operations.
			</p>
			
			<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
				<div class="p-4 rounded-lg bg-muted">
					<h4 class="font-semibold text-text mb-2">In-band SQLi</h4>
					<p class="text-sm text-text-muted">Attacker uses the same channel to launch attack and gather results. Most common type.</p>
				</div>
				<div class="p-4 rounded-lg bg-muted">
					<h4 class="font-semibold text-text mb-2">Blind SQLi</h4>
					<p class="text-sm text-text-muted">No direct output visible. Attacker infers data by observing application behavior or timing.</p>
				</div>
				<div class="p-4 rounded-lg bg-muted">
					<h4 class="font-semibold text-text mb-2">Out-of-band SQLi</h4>
					<p class="text-sm text-text-muted">Data is retrieved via different channel (DNS, HTTP requests to attacker server).</p>
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
						<h3 class="text-base font-semibold text-text">How SQL Injection Works</h3>
						<p class="mt-1 text-sm text-text-muted">See how attackers bypass authentication</p>
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
						<p class="mt-1 text-sm text-text-muted">Try SQL injection on a simulated login form</p>
					</div>
					<div class="flex items-center gap-3">
						<span class="text-sm text-text-muted">Vulnerable Mode:</span>
						<button 
							class={cn(
								"relative w-12 h-6 rounded-full transition-colors",
								isVulnerable ? "bg-danger" : "bg-success"
							)}
							onclick={() => { isVulnerable = !isVulnerable; queryResult = null; }}
							aria-label="Toggle vulnerable mode"
						>
							<span class={cn(
								"absolute top-1 size-4 rounded-full bg-white transition-transform",
								isVulnerable ? "translate-x-1" : "translate-x-7"
							)}></span>
						</button>
					</div>
				</div>
			{/snippet}
			
			{#if !isVulnerable}
				<Alert variant="success" className="mb-4">
					<strong>Protected Mode Active!</strong> Using parameterized queries - SQL injection is not possible.
				</Alert>
			{:else}
				<Alert variant="warning" className="mb-4">
					<strong>Vulnerable Mode!</strong> String concatenation used - try injecting SQL!
				</Alert>
			{/if}
			
			<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<!-- Login Form -->
				<div class="space-y-4">
					<h4 class="font-medium text-text">Login Form</h4>
					
					<div>
						<label class="block text-sm font-medium text-text mb-1.5">Username</label>
						<Input bind:value={username} placeholder="Enter username" />
					</div>
					
					<div>
						<label class="block text-sm font-medium text-text mb-1.5">Password</label>
						<Input bind:value={password} type="password" placeholder="Enter password" />
					</div>
					
					<Button onclick={simulateQuery} fullWidth>
						Login
					</Button>
					
					<div class="space-y-2">
						<p class="text-xs text-text-muted">Try these payloads:</p>
						<div class="flex flex-wrap gap-2">
							<button 
								class="px-2 py-1 text-xs rounded bg-muted hover:bg-border text-text-muted transition-colors"
								onclick={() => { username = "admin' --"; password = "anything"; }}
							>
								admin&apos; --
							</button>
							<button 
								class="px-2 py-1 text-xs rounded bg-muted hover:bg-border text-text-muted transition-colors"
								onclick={() => { username = "' OR '1'='1"; password = "' OR '1'='1"; }}
							>
								&apos; OR &apos;1&apos;=&apos;1
							</button>
							<button 
								class="px-2 py-1 text-xs rounded bg-muted hover:bg-border text-text-muted transition-colors"
								onclick={() => { username = "admin"; password = "super_secret_123"; }}
							>
								Valid Login
							</button>
						</div>
					</div>
				</div>

				<!-- Query Visualization -->
				<div class="space-y-4">
					<h4 class="font-medium text-text">Generated SQL Query</h4>
					<CodeEditor 
						code={generateQuery(username, password, !isVulnerable)} 
						language="sql" 
						readonly 
						title="query.sql"
					/>
					
					{#if queryResult}
						<div>
							<h4 class="font-medium text-text mb-2">Query Result</h4>
							<div class="p-4 rounded-lg bg-canvas border border-border font-mono text-sm overflow-auto max-h-48">
								{#if queryResult.startsWith('[')}
									<div class="text-success">
										{#if isVulnerable && (username.includes("'") || username.includes("--"))}
											<Badge variant="danger" className="mb-2">SQL Injection Successful!</Badge>
										{/if}
										<pre>{queryResult}</pre>
									</div>
								{:else}
									<div class="text-text-muted">{queryResult}</div>
								{/if}
							</div>
						</div>
					{/if}
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
						<span class="text-sm text-text-muted">String concatenation</span>
					</div>
					<CodeEditor code={vulnerableCode} language="javascript" readonly />
				</div>
				<div>
					<div class="flex items-center gap-2 mb-2">
						<Badge variant="success">Safe</Badge>
						<span class="text-sm text-text-muted">Parameterized queries</span>
					</div>
					<CodeEditor code={safeCode} language="javascript" readonly />
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
						<h4 class="font-semibold text-text">Parameterized Queries</h4>
						<p class="text-sm text-text-muted mt-1">Always use prepared statements with bound parameters. This separates SQL code from data, making injection impossible.</p>
					</div>
				</div>
				
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">ORM Usage</h4>
						<p class="text-sm text-text-muted mt-1">Use Object-Relational Mapping (ORM) libraries that handle query building safely. Examples: Prisma, Drizzle, SQLAlchemy.</p>
					</div>
				</div>
				
				<div class="flex gap-4 p-4 rounded-lg bg-muted">
					<div class="size-10 rounded-lg bg-success-soft flex items-center justify-center text-success shrink-0">
						<svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</div>
					<div>
						<h4 class="font-semibold text-text">Least Privilege</h4>
						<p class="text-sm text-text-muted mt-1">Database accounts should have minimal required permissions. Don&apos;t use admin accounts for web applications.</p>
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
						<p class="text-sm text-text-muted mt-1">Validate input type, length, and format. Use allowlists for expected values when possible.</p>
					</div>
				</div>
			</div>
		</Card>
	</section>
</ModuleLayout>
