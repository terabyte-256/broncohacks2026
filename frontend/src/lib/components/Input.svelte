<script lang="ts">
	import type { HTMLInputAttributes } from 'svelte/elements';
	import { cn, uiTokens } from '$lib/theme';

type Props = Omit<HTMLInputAttributes, 'class' | 'value'> & {
	label?: string;
	value?: string;
	error?: string;
	helperText?: string;
	className?: string;
	size?: 'sm' | 'md' | 'lg';
};

	let {
		id,
		label,
		value = $bindable(''),
		error = '',
		helperText = '',
		className = '',
		size = 'md',
		required = false,
		...restProps
	}: Props = $props();

	const sizeClasses = {
		sm: 'px-2.5 py-1.5 text-xs',
		md: 'px-3 py-2.5 text-sm',
		lg: 'px-4 py-3.5 text-base'
	};
</script>

<div class={cn('space-y-1.5', className)}>
	{#if label}
		<label for={id} class="block text-sm font-medium text-text">
			{label}
			{#if required}
				<span class="text-danger"> *</span>
			{/if}
		</label>
	{/if}
	<input
		{id}
		bind:value
		{required}
		class={cn(
			'w-full rounded-lg border border-border bg-surface text-text placeholder:text-text-muted transition-colors',
			sizeClasses[size],
			uiTokens.focusRing,
			error && 'border-danger'
		)}
		aria-invalid={Boolean(error)}
		aria-describedby={id && (helperText || error) ? `${id}-hint` : undefined}
		{...restProps}
	/>
	{#if helperText || error}
		<p id={id ? `${id}-hint` : undefined} class={cn('text-xs', error ? 'text-danger' : 'text-text-muted')}>
			{error || helperText}
		</p>
	{/if}
</div>
