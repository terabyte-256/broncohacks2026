<script lang="ts">
	import type { HTMLTextareaAttributes } from 'svelte/elements';
	import { cn, uiTokens } from '$lib/theme';

type Props = Omit<HTMLTextareaAttributes, 'class' | 'value'> & {
label: string;
value?: string;
error?: string;
helperText?: string;
className?: string;
};

	let {
		id,
label,
value = $bindable(''),
error = '',
helperText = '',
className = '',
required = false,
		rows = 5,
		...restProps
	}: Props = $props();
</script>

<div class={cn('space-y-1.5', className)}>
	<label for={id} class="block text-sm font-medium text-text">
		{label}
{#if required}
<span class="text-danger"> *</span>
{/if}
</label>
<textarea
{id}
bind:value
{required}
{rows}
		class={cn(
			'w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text placeholder:text-text-muted',
			uiTokens.focusRing,
			error && 'border-danger'
		)}
		aria-invalid={Boolean(error)}
		aria-describedby={id && (helperText || error) ? `${id}-hint` : undefined}
		{...restProps}
	></textarea>
	{#if helperText || error}
		<p id={id ? `${id}-hint` : undefined} class={cn('text-xs', error ? 'text-danger' : 'text-text-muted')}>
			{error || helperText}
		</p>
	{/if}
</div>
