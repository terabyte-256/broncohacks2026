<script lang="ts">
	import { onMount } from 'svelte';
	import { Alert, Button, Card, ProgressBar, SectionHeader } from '$lib/components';
	import { getErrorMessage, getTrackModules, getTracks } from '$lib/services';
	import { createAsyncState } from '$lib/stores';

	interface QuizCatalogItem {
		quizId: number;
		moduleId: number;
		trackTitle: string;
		trackId: number;
		moduleTitle: string;
		moduleDescription: string;
		completionPercent: number;
		lastScore: number | null;
		completed: boolean;
	}

	interface TrackGroup {
		trackId: number;
		trackTitle: string;
		quizzes: QuizCatalogItem[];
	}

	const catalogState = createAsyncState<TrackGroup[]>();

	async function loadQuizCatalog() {
		catalogState.setLoading();
		try {
			const { tracks } = await getTracks();
			if (!tracks.length) {
				catalogState.setEmpty('No tracks are available yet.');
				return;
			}

			const moduleResponses = await Promise.all(
				tracks.map((track) => getTrackModules(track.id))
			);

			const groups: TrackGroup[] = moduleResponses
				.map((response, i) => {
					const quizzes: QuizCatalogItem[] = response.modules
						.filter((m) => m.quizId !== null)
						.map((m) => ({
							quizId: m.quizId as number,
							moduleId: m.id,
							trackId: tracks[i].id,
							trackTitle: response.track.title,
							moduleTitle: m.title,
							moduleDescription: m.description,
							completionPercent: m.completionPercent,
							lastScore: m.lastScore,
							completed: m.completed
						}));
					return { trackId: tracks[i].id, trackTitle: response.track.title, quizzes };
				})
				.filter((g) => g.quizzes.length > 0);

			if (!groups.length) {
				catalogState.setEmpty('No quizzes are currently available.');
				return;
			}

			catalogState.setSuccess(groups);
		} catch (error) {
			catalogState.setError(getErrorMessage(error));
		}
	}

	const TRACK_ICONS: Record<number, string> = {
		1: '📧',
		2: '🔐',
		3: '💻'
	};

	onMount(() => {
		void loadQuizCatalog();
	});
</script>

<SectionHeader
	title="Quizzes"
	subtitle="Test your knowledge across all cybersecurity categories."
>
	{#snippet actions()}
		<Button variant="secondary" href="/">← Home</Button>
		<Button variant="secondary" onclick={loadQuizCatalog}>Reload</Button>
	{/snippet}
</SectionHeader>

{#if $catalogState.status === 'loading'}
	<div class="space-y-6">
		{#each [0, 1] as i (i)}
			<div>
				<div class="mb-3 h-5 w-48 animate-pulse rounded bg-muted"></div>
				<div class="grid gap-3 sm:grid-cols-2">
					{#each [0, 1] as j (j)}
						<Card>
							<div class="h-4 w-32 animate-pulse rounded bg-muted"></div>
							<div class="mt-2 h-3 w-full animate-pulse rounded bg-muted"></div>
							<div class="mt-4 h-2 w-full animate-pulse rounded bg-muted"></div>
						</Card>
					{/each}
				</div>
			</div>
		{/each}
	</div>
{:else if $catalogState.status === 'error'}
	<Card>
		<Alert variant="danger" title="Could not load quizzes">{$catalogState.message}</Alert>
	</Card>
{:else if $catalogState.status === 'empty'}
	<Card>
		<Alert variant="warning">{$catalogState.message}</Alert>
	</Card>
{:else if $catalogState.status === 'success' && $catalogState.data}
	<div class="space-y-8">
		{#each $catalogState.data as group (group.trackId)}
			<div>
				<!-- Track heading -->
				<div class="mb-3 flex items-center gap-2">
					<span class="text-xl">{TRACK_ICONS[group.trackId] ?? '📘'}</span>
					<h2 class="text-base font-semibold text-text">{group.trackTitle}</h2>
					<span class="rounded-full bg-muted px-2 py-0.5 text-xs text-text-muted">
						{group.quizzes.length} {group.quizzes.length === 1 ? 'quiz' : 'quizzes'}
					</span>
				</div>

				<!-- Quiz cards -->
				<div class="grid gap-3 sm:grid-cols-2">
					{#each group.quizzes as quiz (quiz.quizId)}
						<div
							class="flex flex-col rounded-xl border border-border bg-surface p-5 shadow-sm"
						>
							<!-- Title + status badge -->
							<div class="mb-2 flex items-start justify-between gap-3">
								<p class="font-semibold text-text">{quiz.moduleTitle}</p>
								{#if quiz.completed}
									<span
										class="shrink-0 rounded-full bg-success-soft px-2.5 py-0.5 text-xs font-medium text-success"
									>
										Completed
									</span>
								{:else if quiz.completionPercent > 0}
									<span
										class="shrink-0 rounded-full bg-brand-soft px-2.5 py-0.5 text-xs font-medium text-brand"
									>
										In progress
									</span>
								{:else}
									<span
										class="shrink-0 rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium text-text-muted"
									>
										Not started
									</span>
								{/if}
							</div>

							<p class="mb-4 text-sm text-text-muted">{quiz.moduleDescription}</p>

							<!-- Progress -->
							<div class="mb-4 space-y-1">
								<ProgressBar
									value={quiz.completionPercent}
									label="{quiz.moduleTitle} progress"
									showValue={false}
								/>
								<div class="flex items-center justify-between text-xs text-text-muted">
									<span>{quiz.completionPercent}% complete</span>
									{#if quiz.lastScore !== null}
										<span>Last score: {quiz.lastScore}%</span>
									{/if}
								</div>
							</div>

							<!-- Action -->
							<div class="mt-auto">
								<Button href="/quiz/{quiz.quizId}" fullWidth>
									{quiz.completed ? 'Retake quiz' : quiz.completionPercent > 0 ? 'Continue quiz' : 'Start quiz'} →
								</Button>
							</div>
						</div>
					{/each}
				</div>
			</div>
		{/each}
	</div>
{/if}
