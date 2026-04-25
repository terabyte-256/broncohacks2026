<script lang="ts">
import { createEventDispatcher } from 'svelte';
import { cn, uiTokens } from '$lib/theme';

type Result = 'neutral' | 'correct' | 'incorrect';

type OptionValue = string | number;

interface Props {
value: OptionValue;
label: string;
description?: string;
selected?: boolean;
result?: Result;
disabled?: boolean;
}

const dispatch = createEventDispatcher<{ select: { value: OptionValue } }>();

let { value, label, description = '', selected = false, result = 'neutral', disabled = false }: Props = $props();

function handleSelect() {
if (!disabled) {
dispatch('select', { value });
}
}
</script>

<button
type="button"
class={cn(
'w-full rounded-lg border px-4 py-3 text-left text-sm transition-colors',
uiTokens.focusRing,
result === 'correct' && 'border-success-border bg-success-soft text-success',
result === 'incorrect' && 'border-danger-border bg-danger-soft text-danger',
result === 'neutral' && selected && 'border-brand-border bg-brand-soft text-brand-strong',
result === 'neutral' && !selected && 'border-border bg-surface text-text hover:bg-muted',
disabled && 'cursor-not-allowed opacity-80'
)}
aria-pressed={selected}
aria-disabled={disabled}
onclick={handleSelect}
>
<div class="font-medium">{label}</div>
{#if description}
<p class="mt-1 text-xs text-text-muted">{description}</p>
{/if}
</button>
