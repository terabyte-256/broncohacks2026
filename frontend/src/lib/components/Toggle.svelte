<script lang="ts">
	import { cn } from '$lib/theme';

	interface Props {
		checked: boolean;
		onLabel?: string;
		offLabel?: string;
		onColor?: 'success' | 'brand' | 'info';
		offColor?: 'danger' | 'warning' | 'muted';
		disabled?: boolean;
		className?: string;
		onchange?: (checked: boolean) => void;
	}

	let { 
		checked = $bindable(false), 
		onLabel = 'On',
		offLabel = 'Off',
		onColor = 'success',
		offColor = 'danger',
		disabled = false,
		className = '',
		onchange
	}: Props = $props();

	const colorClasses = {
		success: 'bg-success border-success focus:ring-success',
		brand: 'bg-brand border-brand focus:ring-brand',
		info: 'bg-info border-info focus:ring-info',
		danger: 'bg-danger border-danger focus:ring-danger',
		warning: 'bg-warning border-warning focus:ring-warning',
		muted: 'bg-muted border-border focus:ring-border'
	};

	const labelColorClasses = {
		success: 'text-success',
		brand: 'text-brand',
		info: 'text-info',
		danger: 'text-danger',
		warning: 'text-warning',
		muted: 'text-text-muted'
	};

	function handleClick() {
		if (disabled) return;
		checked = !checked;
		onchange?.(checked);
	}
</script>

<div class={cn("flex items-center gap-3", className)}>
	<span class={cn(
		"text-sm font-medium transition-colors",
		checked ? labelColorClasses[onColor] : labelColorClasses[offColor]
	)}>
		{checked ? onLabel : offLabel}
	</span>
	<button 
		type="button"
		role="switch"
		aria-checked={checked}
		{disabled}
		class={cn(
			"relative w-14 h-7 rounded-full transition-all duration-200 border-2 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-canvas",
			checked ? colorClasses[onColor] : colorClasses[offColor],
			disabled && "opacity-50 cursor-not-allowed"
		)}
		onclick={handleClick}
	>
		<span class={cn(
			"absolute top-0.5 size-5 rounded-full bg-white shadow-md transition-transform duration-200",
			checked ? "translate-x-7" : "translate-x-0.5"
		)}></span>
	</button>
</div>
</script>
