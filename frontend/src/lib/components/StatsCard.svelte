<script lang="ts">
	import { cn, uiTokens } from '$lib/theme';

	interface Props {
		icon: string;
		value: string | number;
		label: string;
		trend?: { value: number; label: string };
		variant?: 'brand' | 'success' | 'warning' | 'danger' | 'info';
	}

	let { icon, value, label, trend, variant = 'brand' }: Props = $props();

	const bgColors = {
		brand: 'bg-brand-soft',
		success: 'bg-success-soft',
		warning: 'bg-warning-soft',
		danger: 'bg-danger-soft',
		info: 'bg-info-soft'
	};
</script>

<div class={cn(uiTokens.card, 'p-5')}>
	<div class="flex items-start justify-between">
		<div class={cn('flex h-12 w-12 items-center justify-center rounded-xl text-2xl', bgColors[variant])}>
			{icon}
		</div>
		{#if trend}
			<div class={cn(
				'flex items-center gap-1 rounded-full px-2 py-1 text-xs font-medium',
				trend.value >= 0 ? 'bg-success-soft text-success' : 'bg-danger-soft text-danger'
			)}>
				<span>{trend.value >= 0 ? '↑' : '↓'}</span>
				<span>{Math.abs(trend.value)}%</span>
			</div>
		{/if}
	</div>
	<div class="mt-4">
		<p class="text-3xl font-bold tracking-tight text-text">{value}</p>
		<p class="mt-1 text-sm text-text-muted">{label}</p>
	</div>
</div>
