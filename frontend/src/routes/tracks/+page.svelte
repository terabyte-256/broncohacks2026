<script lang="ts">
import { onMount } from 'svelte';
import { Alert, Badge, Button, Card, ProgressBar, SectionHeader } from '$lib/components';
import {
getErrorMessage,
getTrackModules,
getTracks,
type TrackModulesResponse,
type TrackSummary
} from '$lib/services';
import { createAsyncState } from '$lib/stores';

const tracksState = createAsyncState<TrackSummary[]>();
const modulesState = createAsyncState<TrackModulesResponse>();

let selectedTrackId = $state<number | null>(null);

async function loadTracks() {
tracksState.setLoading();
try {
const response = await getTracks();
if (!response.tracks.length) {
tracksState.setEmpty('No learning tracks available yet.');
modulesState.reset();
selectedTrackId = null;
return;
}
tracksState.setSuccess(response.tracks);
const nextTrackId = selectedTrackId ?? response.tracks[0].id;
await loadModules(nextTrackId);
} catch (error) {
tracksState.setError(getErrorMessage(error));
}
}

async function loadModules(trackId: number) {
selectedTrackId = trackId;
modulesState.setLoading();
try {
const response = await getTrackModules(trackId);
if (!response.modules.length) {
modulesState.setEmpty('This track has no modules yet.');
return;
}
modulesState.setSuccess(response);
} catch (error) {
modulesState.setError(getErrorMessage(error));
}
}

onMount(() => {
void loadTracks();
});
</script>

<SectionHeader title="Learning Tracks" subtitle="Browse tracks and inspect module-level progress.">
{#snippet actions()}
<Button variant="secondary" onclick={loadTracks}>Reload tracks</Button>
{/snippet}
</SectionHeader>

<div class="grid gap-5 lg:grid-cols-[2fr_3fr]">
<Card title="Tracks" description="Select a track to inspect modules and quizzes.">
{#if $tracksState.status === 'loading'}
<p class="text-sm text-text-muted">Loading tracks...</p>
{:else if $tracksState.status === 'error'}
<Alert variant="danger">{$tracksState.message}</Alert>
{:else if $tracksState.status === 'empty'}
<Alert variant="warning">{$tracksState.message}</Alert>
{:else if $tracksState.status === 'success' && $tracksState.data}
<ul class="space-y-3">
{#each $tracksState.data as track (track.id)}
<li>
<button
type="button"
class={`w-full rounded-lg border px-3 py-3 text-left transition-colors ${
selectedTrackId === track.id
? 'border-brand-border bg-brand-soft'
: 'border-border bg-surface hover:bg-muted'
}`}
onclick={() => loadModules(track.id)}
>
<div class="flex flex-wrap items-center justify-between gap-2">
<p class="font-medium text-text">{track.title}</p>
<Badge variant={track.completionPercent >= 100 ? 'success' : 'neutral'}>{track.completionPercent}%</Badge>
</div>
<p class="mt-1 text-sm text-text-muted">{track.description}</p>
<div class="mt-2 text-xs text-text-muted">
{track.completedModules}/{track.moduleCount} modules completed
</div>
</button>
</li>
{/each}
</ul>
{/if}
</Card>

<Card title="Modules" description="Modules for the selected track.">
{#if $modulesState.status === 'loading'}
<p class="text-sm text-text-muted">Loading modules...</p>
{:else if $modulesState.status === 'error'}
<Alert variant="danger">{$modulesState.message}</Alert>
{:else if $modulesState.status === 'empty'}
<Alert variant="warning">{$modulesState.message}</Alert>
{:else if $modulesState.status === 'success' && $modulesState.data}
<div class="space-y-3">
<p class="text-sm text-text-muted">{$modulesState.data.track.title}</p>
<ul class="space-y-3">
{#each $modulesState.data.modules as module (module.id)}
<li class="rounded-lg border border-border bg-muted px-3 py-3">
<div class="flex flex-wrap items-center justify-between gap-2">
<p class="font-medium text-text">{module.title}</p>
<Badge variant={module.completed ? 'success' : 'brand'}>{module.completed ? 'completed' : 'in progress'}</Badge>
</div>
<p class="mt-1 text-sm text-text-muted">{module.description}</p>
<div class="mt-2">
<ProgressBar value={module.completionPercent} label={`${module.title} completion`} />
</div>
{#if module.lastScore !== null}
<p class="mt-2 text-xs text-text-muted">Last quiz score: {module.lastScore}%</p>
{/if}
</li>
{/each}
</ul>
</div>
{:else}
<Alert variant="info">Choose a track to view modules.</Alert>
{/if}
</Card>
</div>
