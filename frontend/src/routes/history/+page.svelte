<script lang="ts">
import { onMount } from 'svelte';
import { Alert, Badge, Button, Card, SectionHeader } from '$lib/components';
import { getErrorMessage, getMessageHistory, type MessageHistoryItem } from '$lib/services';
import { createAsyncState } from '$lib/stores';

const historyState = createAsyncState<MessageHistoryItem[]>();

function riskVariant(level: MessageHistoryItem['riskLevel']): 'success' | 'warning' | 'danger' {
if (level === 'Low') {
return 'success';
}
if (level === 'High') {
return 'danger';
}
return 'warning';
}

async function loadHistory() {
historyState.setLoading();
try {
const response = await getMessageHistory();
if (!response.history.length) {
historyState.setEmpty('No message checks have been saved yet.');
return;
}
historyState.setSuccess(response.history);
} catch (error) {
historyState.setError(getErrorMessage(error));
}
}

onMount(() => {
void loadHistory();
});
</script>

<SectionHeader title="History" subtitle="Review analyzed messages and outcomes.">
{#snippet actions()}
<Button variant="secondary" onclick={loadHistory}>Reload history</Button>
{/snippet}
</SectionHeader>

<Card>
{#if $historyState.status === 'loading'}
<p class="text-sm text-text-muted">Loading message history...</p>
{:else if $historyState.status === 'error'}
<Alert variant="danger" title="Could not load history">{$historyState.message}</Alert>
{:else if $historyState.status === 'empty'}
<Alert variant="warning">{$historyState.message}</Alert>
{:else if $historyState.status === 'success' && $historyState.data}
<ul class="space-y-3">
{#each $historyState.data as item (item.id)}
<li class="rounded-lg border border-border bg-muted px-3 py-3">
<div class="flex flex-wrap items-center justify-between gap-2">
<div class="flex items-center gap-2">
<Badge variant={riskVariant(item.riskLevel)}>{item.riskLevel}</Badge>
<p class="text-sm text-text-muted">{item.verdict}</p>
</div>
<p class="text-xs text-text-muted">{new Date(item.createdAt).toLocaleString()}</p>
</div>
<p class="mt-2 text-sm text-text">{item.message}</p>
<p class="mt-1 text-sm text-text-muted">{item.explanation}</p>
{#if item.redFlags.length}
<ul class="mt-2 list-disc pl-5 text-xs text-text-muted">
{#each item.redFlags as flag, index (`${item.id}-flag-${index}`)}
<li>{flag}</li>
{/each}
</ul>
{/if}
</li>
{/each}
</ul>
{/if}
</Card>
