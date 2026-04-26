<script lang="ts">
	import { cn } from '$lib/theme';

	interface Step {
		icon: string;
		label: string;
		description: string;
	}

	interface Props {
		steps: Step[];
		currentStep?: number;
		title?: string;
		className?: string;
	}

	let { steps, currentStep = -1, title, className = '' }: Props = $props();
</script>

<div class={cn("rounded-lg border border-border bg-surface p-6", className)}>
	{#if title}
		<h4 class="text-sm font-semibold text-text mb-4">{title}</h4>
	{/if}
	
	<div class="relative">
		<!-- Connection line -->
		<div class="absolute top-6 left-6 right-6 h-0.5 bg-border" aria-hidden="true"></div>
		
		<!-- Steps -->
		<div class="relative flex justify-between">
			{#each steps as step, index}
				{@const isActive = index <= currentStep}
				{@const isCurrent = index === currentStep}
				
				<div class="flex flex-col items-center gap-2 relative">
					<!-- Step circle -->
					<div 
						class={cn(
							"size-12 rounded-full flex items-center justify-center text-xl transition-all duration-300 border-2",
							isActive 
								? "bg-brand border-brand text-white scale-110" 
								: "bg-muted border-border text-text-muted",
							isCurrent && "ring-4 ring-brand/30"
						)}
					>
						{step.icon}
					</div>
					
					<!-- Label -->
					<span class={cn(
						"text-xs font-medium text-center max-w-20 transition-colors",
						isActive ? "text-text" : "text-text-muted"
					)}>
						{step.label}
					</span>
					
					<!-- Description tooltip -->
					{#if isCurrent}
						<div 
							class="absolute top-full mt-3 px-3 py-2 rounded-lg bg-brand text-white text-xs max-w-32 text-center shadow-lg"
							style="animation: fadeIn 0.2s ease-out;"
						>
							{step.description}
							<div class="absolute -top-1 left-1/2 -translate-x-1/2 size-2 bg-brand rotate-45"></div>
						</div>
					{/if}
				</div>
			{/each}
		</div>
	</div>
</div>
