<script lang="ts">
	import { Button } from '$lib/components';
	import { cn, uiTokens } from '$lib/theme';
</script>

<svelte:head>
	<title>Authentication Error | CyberLearn</title>
</svelte:head>

<div class="flex min-h-[60vh] flex-col items-center justify-center">
	<div class={cn(uiTokens.card, 'max-w-md p-8 text-center')}>
		<div class="mb-4 text-5xl">⚠️</div>
		<h1 class="mb-2 text-2xl font-bold text-text">Authentication Error</h1>
		<p class="mb-6 text-text-muted">
			Something went wrong during sign in. Please try again.
		</p>
		<Button href="/auth/login" variant="primary">
			Try Again
		</Button>
	</div>
</div>
