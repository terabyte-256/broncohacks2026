<script lang="ts">
import { onMount } from 'svelte';
import { Alert, Badge, Button, Card, ProgressBar, SectionHeader } from '$lib/components';
import { getDashboard, getErrorMessage, getProgress, type DashboardData, type ProgressData } from '$lib/services';
import { createAsyncState } from '$lib/stores';

const dashboardState = createAsyncState<DashboardData>();
const progressState = createAsyncState<ProgressData>();

let refreshing = $state(false);

const metricCards = $derived.by(() => {
const metrics = $dashboardState.data?.metrics;
if (!metrics) {
return [] as { label: string; value: string; detail?: string }[];
}

return [
{ label: 'Tracks completed', value: `${metrics.completedTracks}/${metrics.totalTracks}` },
{ label: 'Modules completed', value: `${metrics.completedModules}/${metrics.totalModules}` },
{ label: 'Average quiz score', value: `${metrics.averageQuizScore}%` },
{ label: 'Current streak', value: `${metrics.streakDays} day${metrics.streakDays === 1 ? '' : 's'}` }
];
});

async function loadDashboard() {
dashboardState.setLoading();
try {
const dashboard = await getDashboard();
const hasAnyData =
dashboard.metrics.totalTracks > 0 ||
dashboard.metrics.totalModules > 0 ||
dashboard.recentQuizAttempts.length > 0 ||
dashboard.trackProgress.length > 0;

if (!hasAnyData) {
dashboardState.setEmpty('No dashboard data available yet.');
return;
}
dashboardState.setSuccess(dashboard);
} catch (error) {
dashboardState.setError(getErrorMessage(error));
}
}

async function loadProgress() {
progressState.setLoading();
try {
const progress = await getProgress();
if (!progress.modules.length && progress.summary.totalModules === 0) {
progressState.setEmpty('No progress has been recorded yet.');
return;
}
progressState.setSuccess(progress);
} catch (error) {
progressState.setError(getErrorMessage(error));
}
}

async function refreshAll() {
refreshing = true;
await Promise.all([loadDashboard(), loadProgress()]);
refreshing = false;
}

onMount(() => {
void refreshAll();
});
</script>

<SectionHeader title="Home Dashboard" subtitle="Overview of learner momentum and track progress.">
{#snippet actions()}
<Button variant="secondary" onclick={refreshAll} loading={refreshing}>Refresh</Button>
{/snippet}
</SectionHeader>

{#if $dashboardState.status === 'loading' || $progressState.status === 'loading'}
<div class="grid gap-4 md:grid-cols-2 xl:grid-cols-4" aria-live="polite">
{#each [0, 1, 2, 3] as index (index)}
<Card className="animate-pulse">
<div class="h-4 w-24 rounded bg-muted"></div>
<div class="mt-3 h-7 w-16 rounded bg-muted"></div>
</Card>
{/each}
</div>
{:else if $dashboardState.status === 'error' || $progressState.status === 'error'}
<div class="space-y-4">
<Alert variant="danger" title="Could not load dashboard">
{$dashboardState.message || $progressState.message || 'Please try again.'}
</Alert>
<Button variant="secondary" onclick={refreshAll}>Try again</Button>
</div>
{:else if $dashboardState.status === 'empty' && $progressState.status === 'empty'}
<Alert variant="warning" title="No activity yet">
Start a learning track or complete a quiz to populate this dashboard.
</Alert>
{:else}
<div class="space-y-5">
<div class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
{#each metricCards as metric (metric.label)}
<Card title={metric.label}>
<p class="text-2xl font-semibold text-text">{metric.value}</p>
{#if metric.detail}
<p class="mt-1 text-sm text-text-muted">{metric.detail}</p>
{/if}
</Card>
{/each}
</div>

<div class="grid gap-4 lg:grid-cols-2">
<Card title="Recent quiz attempts" description="Latest quiz submissions from the backend dashboard feed.">
{#if $dashboardState.data?.recentQuizAttempts.length}
<ul class="space-y-2 text-sm">
{#each $dashboardState.data.recentQuizAttempts as attempt (attempt.id)}
<li class="rounded-md border border-border bg-muted px-3 py-2">
<div class="flex items-center justify-between gap-2">
<p class="font-medium text-text">{attempt.quizTitle}</p>
<Badge variant={attempt.score >= 70 ? 'success' : 'warning'}>{attempt.score}%</Badge>
</div>
<p class="mt-1 text-xs text-text-muted">{new Date(attempt.submittedAt).toLocaleString()}</p>
</li>
{/each}
</ul>
{:else}
<Alert variant="info">No quiz attempts yet.</Alert>
{/if}
</Card>

<Card title="Track progress" description="Completion percentages across all learning tracks.">
{#if $dashboardState.data?.trackProgress.length}
<ul class="space-y-3">
{#each $dashboardState.data.trackProgress as track (track.id)}
<li>
<div class="mb-1 flex items-center justify-between gap-2 text-sm">
<p class="font-medium text-text">{track.title}</p>
<span class="text-text-muted">{track.completionPercent}%</span>
</div>
<ProgressBar value={track.completionPercent} label={track.title} showValue={false} />
</li>
{/each}
</ul>
{:else}
<Alert variant="info">Track progress will appear after activity.</Alert>
{/if}
</Card>
</div>

<Card title="Overall progress" description="Summary from GET /api/progress.">
{#if $progressState.status === 'success' && $progressState.data}
<div class="space-y-4">
<ProgressBar value={$progressState.data.summary.averageCompletionPercent} label="Average completion" />
<div class="grid grid-cols-2 gap-3 text-sm">
<div>
<p class="text-text-muted">Completed modules</p>
<p class="font-semibold text-text">
{$progressState.data.summary.completedModules}/{$progressState.data.summary.totalModules}
</p>
</div>
<div>
<p class="text-text-muted">Tracked modules</p>
<p class="font-semibold text-text">{$progressState.data.modules.length}</p>
</div>
</div>
</div>
{:else if $progressState.status === 'empty'}
<Alert variant="warning">{$progressState.message}</Alert>
{:else}
<Alert variant="info">Progress data is unavailable.</Alert>
{/if}
</Card>
</div>
{/if}
