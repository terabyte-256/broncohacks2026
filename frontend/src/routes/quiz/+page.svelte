<script lang="ts">
import { onMount } from 'svelte';
import { resolve } from '$app/paths';
import { Alert, Button, Card, SectionHeader } from '$lib/components';
import { getErrorMessage, getTrackModules, getTracks } from '$lib/services';
import { createAsyncState } from '$lib/stores';

interface QuizCatalogItem {
quizId: number;
trackTitle: string;
moduleTitle: string;
moduleDescription: string;
}

const quizzesState = createAsyncState<QuizCatalogItem[]>();

async function loadQuizCatalog() {
quizzesState.setLoading();
try {
const { tracks } = await getTracks();
if (!tracks.length) {
quizzesState.setEmpty('No tracks are available yet.');
return;
}

const moduleResponses = await Promise.all(tracks.map((track) => getTrackModules(track.id)));
const quizzes = moduleResponses.flatMap((response) =>
response.modules
.filter((module) => module.quizId !== null)
.map((module) => ({
quizId: module.quizId as number,
trackTitle: response.track.title,
moduleTitle: module.title,
moduleDescription: module.description
}))
);

if (!quizzes.length) {
quizzesState.setEmpty('No quizzes are currently available.');
return;
}

quizzesState.setSuccess(quizzes);
} catch (error) {
quizzesState.setError(getErrorMessage(error));
}
}

onMount(() => {
void loadQuizCatalog();
});
</script>

<SectionHeader title="Quiz" subtitle="Choose a quiz sourced from track/module backend data.">
{#snippet actions()}
<Button variant="secondary" onclick={loadQuizCatalog}>Reload quizzes</Button>
{/snippet}
</SectionHeader>

<Card>
{#if $quizzesState.status === 'loading'}
<p class="text-sm text-text-muted">Loading quizzes...</p>
{:else if $quizzesState.status === 'error'}
<Alert variant="danger" title="Could not load quizzes">{$quizzesState.message}</Alert>
{:else if $quizzesState.status === 'empty'}
<Alert variant="warning">{$quizzesState.message}</Alert>
{:else if $quizzesState.status === 'success' && $quizzesState.data}
<ul class="space-y-3">
{#each $quizzesState.data as quiz (`${quiz.quizId}-${quiz.moduleTitle}`)}
<li class="rounded-lg border border-border bg-muted px-3 py-3">
<p class="font-medium text-text">{quiz.moduleTitle}</p>
<p class="mt-1 text-sm text-text-muted">{quiz.trackTitle}</p>
<p class="mt-1 text-sm text-text-muted">{quiz.moduleDescription}</p>
<div class="mt-3">
<a
href={resolve(`/quiz/${quiz.quizId}`)}
class="inline-flex items-center justify-center rounded-lg bg-brand px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-brand-strong"
>
Start quiz
</a>
</div>
</li>
{/each}
</ul>
{/if}
</Card>
