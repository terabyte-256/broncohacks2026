<script lang="ts">
import { cn } from '$lib/theme';

	interface Props {
value: number;
max?: number;
label?: string;
className?: string;
showValue?: boolean;
}

	let { value, max = 100, label = 'Progress', className = '', showValue = true }: Props = $props();

	const safeValue = $derived(Math.max(0, Math.min(value, max)));
	const percentage = $derived(max > 0 ? Math.round((safeValue / max) * 100) : 0);
</script>

<div class={cn('space-y-2', className)}>
<div class="flex items-center justify-between text-sm">
<span class="font-medium text-text">{label}</span>
{#if showValue}
<span class="text-text-muted">{percentage}%</span>
{/if}
</div>
<div class="h-2.5 w-full overflow-hidden rounded-full bg-muted" role="progressbar" aria-label={label} aria-valuemin={0} aria-valuemax={max} aria-valuenow={safeValue}>
<div class="h-full rounded-full bg-brand transition-all duration-300" style={`width: ${percentage}%;`}></div>
</div>
</div>
