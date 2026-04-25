<script lang="ts">
	import { onMount } from "svelte";
	import { Alert } from "$lib/components";
	import {
		analyzeMessage,
		getDashboard,
		getErrorMessage,
		getProgress,
		type DashboardData,
		type ProgressData,
	} from "$lib/services";
	import { createAsyncState } from "$lib/stores";

	const dashboardState = createAsyncState<DashboardData>();
	const progressState = createAsyncState<ProgressData>();

	let messageText = $state("");
	let analyzing = $state(false);
	let analyzeError = $state("");

	const metrics = $derived($dashboardState.data?.metrics);
	const progressSummary = $derived($progressState.data?.summary);

	async function loadAll() {
		dashboardState.setLoading();
		progressState.setLoading();
		try {
			const [dashboard, progress] = await Promise.all([
				getDashboard(),
				getProgress(),
			]);
			dashboardState.setSuccess(dashboard);
			progressState.setSuccess(progress);
		} catch (error) {
			dashboardState.setError(getErrorMessage(error));
			progressState.setError(getErrorMessage(error));
		}
	}

	async function handleAnalyze() {
		if (!messageText.trim() || analyzing) return;
		analyzing = true;
		analyzeError = "";
		try {
			const result = await analyzeMessage({
				message: messageText.trim(),
			});
			sessionStorage.setItem("cl_analysis", JSON.stringify(result));
			sessionStorage.setItem(
				"cl_preview",
				messageText.trim().slice(0, 120),
			);
			window.location.href = "/message-checker";
		} catch (error) {
			analyzeError = getErrorMessage(error);
		} finally {
			analyzing = false;
		}
	}

	onMount(() => {
		void loadAll();
	});
</script>

<!-- Hero -->
<div class="mb-8 py-4 text-center">
	<h1 class="text-4xl font-bold tracking-tight sm:text-5xl">
		<span class="text-brand">Learn.</span>
		<span class="text-text"> Practice.</span>
		<span class="text-warning"> Stay Safe.</span>
	</h1>
	<p class="mx-auto mt-3 max-w-lg text-base text-text-muted">
		Choose your track and level up your cybersecurity skills or check
		suspicious messages with AI.
	</p>
</div>

<!-- Track + checker cards -->
<div class="mb-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
	<!-- Beginner Track -->
	<a
		href="/tracks/beginner"
		class="group block rounded-xl border border-border bg-surface p-5 shadow-sm transition-all hover:border-brand-border hover:shadow-md"
	>
		<div class="mb-3 flex items-center gap-3">
			<div
				class="flex h-10 w-10 items-center justify-center rounded-lg bg-brand-soft text-xl"
			>
				🎓
			</div>
			<div>
				<p class="font-semibold text-text">Beginner Track</p>
				<p class="text-xs text-text-muted">
					Everyday threat awareness
				</p>
			</div>
		</div>
		<p class="mb-4 text-sm text-text-muted">
			Learn the basics and spot everyday online threats through quick
			quizzes.
		</p>
		<p
			class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand"
		>
			Categories
		</p>
		<div class="space-y-1.5">
			{#each [['🎣', 'Phishing'], ['🧠', 'Social Engineering'], ['🔐', 'Auth & Passwords'], ['🍪', 'Sessions']] as [icon, label]}
				<div
					class="flex items-center justify-between rounded-lg border border-border bg-muted px-3 py-2 text-sm text-text"
				>
					<div class="flex items-center gap-2">
						<span>{icon}</span>
						{label}
					</div>
					<span class="text-text-muted">›</span>
				</div>
			{/each}
		</div>
		<div
			class="mt-4 w-full rounded-lg bg-brand py-2.5 text-center text-sm font-semibold text-white transition-opacity group-hover:opacity-90"
		>
			Start Beginner Track →
		</div>
	</a>

	<!-- Developer Track -->
	<a
		href="/tracks/developer"
		class="group block rounded-xl border border-border bg-surface p-5 shadow-sm transition-all hover:border-brand-border hover:shadow-md"
	>
		<div class="mb-3 flex items-center gap-3">
			<div
				class="flex h-10 w-10 items-center justify-center rounded-lg bg-info-soft text-xl"
			>
				💻
			</div>
			<div>
				<p class="font-semibold text-text">Developer Track</p>
				<p class="text-xs text-text-muted">
					Secure coding fundamentals
				</p>
			</div>
		</div>
		<p class="mb-4 text-sm text-text-muted">
			Explore real-world attack techniques and learn how to build secure
			code.
		</p>
		<p
			class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand"
		>
			Categories
		</p>
		<div class="space-y-1.5">
			<div
				class="flex items-center justify-between rounded-lg border border-border bg-muted px-3 py-2 text-sm text-text"
			>
				<div class="flex items-center gap-2">
					<span
						class="rounded bg-danger-soft px-1.5 py-0.5 text-[10px] font-bold text-danger"
						>XSS</span
					>
					Cross-Site Scripting
				</div>
				<span class="text-text-muted">›</span>
			</div>
			<div
				class="flex items-center justify-between rounded-lg border border-border bg-muted px-3 py-2 text-sm text-text"
			>
				<div class="flex items-center gap-2">
					<span
						class="rounded bg-success-soft px-1.5 py-0.5 text-[10px] font-bold text-success"
						>SQLi</span
					>
					SQL Injection
				</div>
				<span class="text-text-muted">›</span>
			</div>
			<div
				class="flex items-center justify-between rounded-lg border border-border bg-muted px-3 py-2 text-sm text-text"
			>
				<div class="flex items-center gap-2">
					<span
						class="rounded bg-warning-soft px-1.5 py-0.5 text-[10px] font-bold text-warning"
						>CSRF</span
					>
					Cross-Site Request Forgery
				</div>
				<span class="text-text-muted">›</span>
			</div>
		</div>
		<div
			class="mt-4 w-full rounded-lg bg-info py-2.5 text-center text-sm font-semibold text-white transition-opacity group-hover:opacity-90"
		>
			Start Developer Track →
		</div>
	</a>

	<!-- AI Message Checker -->
	<div class="rounded-xl border border-border bg-surface p-5 shadow-sm">
		<div class="mb-3 flex items-center gap-3">
			<div
				class="flex h-10 w-10 items-center justify-center rounded-lg bg-success-soft text-xl"
			>
				🔍
			</div>
			<div>
				<p class="font-semibold text-text">Check Suspicious Message</p>
				<p class="text-xs text-text-muted">AI-powered scam detection</p>
			</div>
		</div>
		<p class="mb-3 text-sm text-text-muted">
			Paste any message (SMS, email, DM, etc.) and let AI tell you if it
			looks suspicious.
		</p>
		<textarea
			bind:value={messageText}
			rows="4"
			maxlength="1000"
			placeholder="Paste the suspicious message here…"
			class="w-full resize-none rounded-lg border border-border bg-muted px-3 py-2 text-sm text-text placeholder:text-text-muted focus:border-brand-border focus:outline-none"
		></textarea>
		<p class="mt-1 text-right text-xs text-text-muted">
			{messageText.length}/1000
		</p>
		{#if analyzeError}
			<div class="mt-2">
				<Alert variant="danger">{analyzeError}</Alert>
			</div>
		{/if}
		<div class="mt-3">
			<button
				onclick={handleAnalyze}
				disabled={!messageText.trim() || analyzing}
				class="w-full rounded-lg bg-success py-2.5 text-sm font-semibold text-canvas transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
			>
				{#if analyzing}
					Analyzing…
				{:else}
					✦ Analyze Message
				{/if}
			</button>
		</div>
		<p class="mt-2 flex items-center gap-1 text-xs text-text-muted">
			<span class="text-success">✓</span> AI analyzes messages securely.
			Your data is not stored or shared.
		</p>
	</div>
</div>

<!-- Bottom stats bar -->
<div class="rounded-xl border border-border bg-surface px-6 py-5">
	<div class="grid grid-cols-2 gap-6 sm:grid-cols-4">
		<div class="flex items-center gap-3">
			<div
				class="flex h-10 w-10 items-center justify-center rounded-full bg-warning-soft text-xl"
			>
				🏆
			</div>
			<div>
				<p class="text-xl font-semibold text-text">
					{metrics?.averageQuizScore ?? 0}
				</p>
				<p class="text-xs text-text-muted">Total Score</p>
			</div>
		</div>
		<div class="flex items-center gap-3">
			<div
				class="flex h-10 w-10 items-center justify-center rounded-full bg-danger-soft text-xl"
			>
				🔥
			</div>
			<div>
				<p class="text-xl font-semibold text-text">
					{metrics?.streakDays ?? 0}
				</p>
				<p class="text-xs text-text-muted">Current Streak</p>
			</div>
		</div>
		<div class="flex items-center gap-3">
			<div
				class="flex h-10 w-10 items-center justify-center rounded-full bg-info-soft text-xl"
			>
				📋
			</div>
			<div>
				<p class="text-xl font-semibold text-text">
					{metrics?.completedModules ?? 0}
				</p>
				<p class="text-xs text-text-muted">Topics Completed</p>
			</div>
		</div>
		<div class="flex items-center gap-3">
			<div
				class="flex h-10 w-10 items-center justify-center rounded-full bg-success-soft text-xl"
			>
				📊
			</div>
			<div>
				<p class="text-xl font-semibold text-text">
					{progressSummary?.averageCompletionPercent ?? 0}%
				</p>
				<p class="text-xs text-text-muted">Overall Progress</p>
			</div>
		</div>
	</div>
</div>
