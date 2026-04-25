<script lang="ts">
	import { onMount } from "svelte";
	import {
		Alert,
		Button,
		Card,
		ProgressBar,
		SectionHeader,
	} from "$lib/components";
	import {
		getErrorMessage,
		getTrackModules,
		type TrackModulesResponse,
	} from "$lib/services";
	import { createAsyncState } from "$lib/stores";

	// Track 1 = "Message and Email Defense" from your seed
	const TRACK_ID = 1;

	const trackState = createAsyncState<TrackModulesResponse>();

	async function loadModules() {
		trackState.setLoading();
		try {
			const response = await getTrackModules(TRACK_ID);
			if (!response.modules.length) {
				trackState.setEmpty(
					"This track has no modules yet.",
				);
				return;
			}
			trackState.setSuccess(response);
		} catch (error) {
			trackState.setError(getErrorMessage(error));
		}
	}

	onMount(() => {
		void loadModules();
	});
</script>

<SectionHeader
	title="Beginner Track"
	subtitle="Learn the basics and spot everyday online threats through quick quizzes."
>
	{#snippet actions()}
		<Button variant="secondary" href="/">← Home</Button>
		<Button variant="secondary" onclick={loadModules}>Reload</Button
		>
	{/snippet}
</SectionHeader>

{#if $trackState.status === "loading"}
	<div class="grid gap-4 sm:grid-cols-2" aria-live="polite">
		{#each [0, 1] as i (i)}
			<Card>
				<div
					class="h-4 w-32 animate-pulse rounded bg-muted"
				></div>
				<div
					class="mt-2 h-3 w-48 animate-pulse rounded bg-muted"
				></div>
				<div
					class="mt-4 h-2 w-full animate-pulse rounded bg-muted"
				></div>
			</Card>
		{/each}
	</div>
{:else if $trackState.status === "error"}
	<Card>
		<Alert variant="danger" title="Could not load modules"
			>{$trackState.message}</Alert
		>
	</Card>
{:else if $trackState.status === "empty"}
	<Card>
		<Alert variant="warning">{$trackState.message}</Alert>
	</Card>
{:else if $trackState.status === "success" && $trackState.data}
	<div class="grid gap-4 sm:grid-cols-2">
		{#each $trackState.data.modules as module (module.id)}
			<a
				href="/tracks/beginner/{module.id}"
				class="group block rounded-xl border border-border bg-surface p-5 shadow-sm transition-all hover:border-brand-border hover:shadow-md"
			>
				<div
					class="mb-3 flex items-start justify-between gap-3"
				>
					<p class="font-semibold text-text">
						{module.title}
					</p>
					{#if module.completed}
						<span
							class="rounded-full bg-success-soft px-2.5 py-0.5 text-xs font-medium text-success"
						>
							Completed
						</span>
					{:else if module.completionPercent > 0}
						<span
							class="rounded-full bg-brand-soft px-2.5 py-0.5 text-xs font-medium text-brand"
						>
							In progress
						</span>
					{:else}
						<span
							class="rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium text-text-muted"
						>
							Not started
						</span>
					{/if}
				</div>

				<p class="mb-4 text-sm text-text-muted">
					{module.description}
				</p>

				<div class="space-y-2">
					<ProgressBar
						value={module.completionPercent}
						label="{module.title} completion"
						showValue={false}
					/>
					<div
						class="flex items-center justify-between text-xs text-text-muted"
					>
						<span
							>{module.completionPercent}%
							complete</span
						>
						{#if module.lastScore !== null}
							<span
								>Last score: {module.lastScore}%</span
							>
						{/if}
					</div>
				</div>

				<div
					class="mt-4 flex items-center gap-1 text-sm font-medium text-brand-strong group-hover:underline"
				>
					{module.completed
						? "Review module"
						: "Start module"}
					<span aria-hidden="true">→</span>
				</div>
			</a>
		{/each}
	</div>
{/if}
