<script lang="ts">
import { onMount } from 'svelte';
import {
Alert,
Badge,
Button,
Card,
SectionHeader,
Textarea,
} from '$lib/components';
import {
analyzeMessage,
getErrorMessage,
type MessageAnalysis,
} from '$lib/services';
import { createAsyncState } from '$lib/stores';

const analysisState = createAsyncState<MessageAnalysis>();
let message = $state('');

function riskVariant(level: MessageAnalysis['riskLevel']): 'success' | 'warning' | 'danger' {
if (level === 'Low') return 'success';
if (level === 'High') return 'danger';
return 'warning';
}

async function submitMessageAnalysis() {
if (!message.trim()) {
analysisState.setEmpty('Enter a message before running analysis.');
return;
}
analysisState.setLoading();
try {
const result = await analyzeMessage({ message });
analysisState.setSuccess(result, 'Analysis complete.');
} catch (error) {
analysisState.setError(getErrorMessage(error));
}
}

function reset() {
message = '';
analysisState.reset();
}

onMount(() => {
const stored = sessionStorage.getItem('cl_analysis');
const preview = sessionStorage.getItem('cl_preview');
sessionStorage.removeItem('cl_analysis');
sessionStorage.removeItem('cl_preview');
if (stored) {
try {
const result = JSON.parse(stored) as MessageAnalysis;
if (preview) message = preview;
analysisState.setSuccess(result, 'Analysis complete.');
} catch {
// ignore malformed data
}
}
});
</script>

<SectionHeader
title="AI Message Checker"
subtitle="Scan suspicious messages and review neutral guidance."
>
{#snippet actions()}
<Button variant="secondary" onclick={reset}>Reset</Button>
{/snippet}
</SectionHeader>

<div class="grid gap-5 lg:grid-cols-[3fr_2fr]">
<Card
title="Message input"
description="Paste a message to analyze for phishing indicators."
>
<form
class="space-y-3"
onsubmit={(event) => {
event.preventDefault();
void submitMessageAnalysis();
}}
>
<Textarea
id="message-input"
label="Message"
bind:value={message}
placeholder="Example: We noticed suspicious login attempts. Click this urgent link to secure your account now."
helperText="Use realistic samples. Avoid sensitive personal data in this demo."
required
/>
<Button type="submit" loading={$analysisState.status === 'loading'}
>Analyze message</Button
>
</form>
</Card>

<Card
title="Analysis result"
description="Result from POST /api/analyze-message."
>
{#if $analysisState.status === 'idle'}
<Alert variant="info">Run an analysis to see safety guidance.</Alert>
{:else if $analysisState.status === 'loading'}
<p class="text-sm text-text-muted">Analyzing message...</p>
{:else if $analysisState.status === 'error'}
<Alert variant="danger" title="Analysis failed">{$analysisState.message}</Alert>
{:else if $analysisState.status === 'empty'}
<Alert variant="warning">{$analysisState.message}</Alert>
{:else if $analysisState.status === 'success' && $analysisState.data}
<div class="space-y-3">
<div class="flex items-center gap-2">
<Badge variant={riskVariant($analysisState.data.riskLevel)}
>{$analysisState.data.riskLevel}</Badge
>
<p class="text-sm text-text-muted">{$analysisState.data.verdict}</p>
</div>
<p class="text-sm text-text">{$analysisState.data.explanation}</p>
<div>
<p class="text-xs font-semibold uppercase tracking-wide text-text-muted">
Red flags
</p>
{#if $analysisState.data.redFlags.length}
<ul class="mt-2 space-y-1 text-sm">
{#each $analysisState.data.redFlags as flag, index (`${flag}-${index}`)}
<li class="rounded-md border border-border bg-muted px-2.5 py-1.5">
{flag}
</li>
{/each}
</ul>
{:else}
<p class="mt-2 text-sm text-text-muted">No red flags returned.</p>
{/if}
</div>
<div>
<p class="text-xs font-semibold uppercase tracking-wide text-text-muted">Tips</p>
{#if $analysisState.data.tips.length}
<ul class="mt-2 list-disc space-y-1 pl-5 text-sm text-text">
{#each $analysisState.data.tips as tip, index (`${tip}-${index}`)}
<li>{tip}</li>
{/each}
</ul>
{:else}
<p class="mt-2 text-sm text-text-muted">No tips returned.</p>
{/if}
</div>
</div>
{/if}
</Card>
</div>
