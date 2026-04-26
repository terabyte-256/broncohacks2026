<script lang="ts">
	import { cn } from '$lib/theme';
	import { onMount } from 'svelte';

	interface Props {
		html: string;
		title?: string;
		className?: string;
		height?: string;
		onAlert?: (message: string) => void;
		showAlertBanner?: boolean;
	}

	let { html, title = 'Preview', className = '', height = 'h-80', onAlert, showAlertBanner = true }: Props = $props();
	
	let iframeRef: HTMLIFrameElement;
	let alertMessage = $state<string | null>(null);
	let alertVisible = $state(false);

	function renderSandbox() {
		if (!iframeRef) return;
		
		// Create a safe sandbox with alert interception
		const sandboxContent = `
			<!DOCTYPE html>
			<html>
			<head>
				<style>
					* { box-sizing: border-box; }
					body { 
						font-family: system-ui, -apple-system, sans-serif;
						padding: 16px;
						margin: 0;
						background: #0a0a0f;
						color: #e4e4e7;
						font-size: 14px;
						line-height: 1.5;
					}
					input, button, textarea, select {
						font-family: inherit;
						font-size: inherit;
						padding: 8px 12px;
						border-radius: 6px;
						border: 1px solid #27272a;
						background: #18181b;
						color: #e4e4e7;
					}
					input:focus, textarea:focus, select:focus {
						outline: none;
						border-color: #22d3ee;
					}
					button {
						background: #22d3ee;
						color: #0a0a0f;
						border: none;
						cursor: pointer;
						font-weight: 500;
					}
					button:hover {
						background: #06b6d4;
					}
					form {
						display: flex;
						flex-direction: column;
						gap: 12px;
					}
					label {
						display: flex;
						flex-direction: column;
						gap: 4px;
						font-size: 13px;
						color: #a1a1aa;
					}
					.comment { color: #6b7280; margin: 8px 0; }
					h1, h2, h3 { color: #f4f4f5; margin: 0 0 12px 0; }
					a { color: #22d3ee; }
				</style>
				<script>
					// Intercept alert and send to parent
					window.alert = function(msg) {
						window.parent.postMessage({ type: 'sandbox-alert', message: String(msg) }, '*');
					};
					
					// Intercept console.log
					const originalLog = console.log;
					console.log = function(...args) {
						window.parent.postMessage({ type: 'sandbox-log', message: args.join(' ') }, '*');
						originalLog.apply(console, args);
					};
				<\/script>
			</head>
			<body>${html}</body>
			</html>
		`;
		
		const blob = new Blob([sandboxContent], { type: 'text/html' });
		iframeRef.src = URL.createObjectURL(blob);
	}

	function handleMessage(event: MessageEvent) {
		if (event.data?.type === 'sandbox-alert') {
			alertMessage = event.data.message;
			alertVisible = true;
			onAlert?.(event.data.message);
			
			// Auto-hide after 3 seconds
			setTimeout(() => {
				alertVisible = false;
			}, 3000);
		}
	}

	onMount(() => {
		window.addEventListener('message', handleMessage);
		return () => window.removeEventListener('message', handleMessage);
	});

	$effect(() => {
		html; // Track html changes
		renderSandbox();
	});
</script>

<div class={cn("rounded-lg border border-border bg-canvas overflow-hidden", className)}>
	<div class="flex items-center justify-between border-b border-border bg-muted px-4 py-2">
		<div class="flex items-center gap-2">
			<div class="size-2 rounded-full bg-success animate-pulse"></div>
			<span class="text-xs font-medium text-text-muted">{title}</span>
		</div>
		<span class="text-xs text-text-muted">Sandboxed Environment</span>
	</div>
	
	<!-- Alert Banner -->
	{#if showAlertBanner && alertVisible && alertMessage}
		<div class="bg-danger text-white px-4 py-2 text-sm font-medium flex items-center gap-2 animate-pulse">
			<svg class="size-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
			</svg>
			<span>XSS Alert Triggered: {alertMessage}</span>
		</div>
	{/if}
	
	<iframe
		bind:this={iframeRef}
		title="Demo Sandbox"
		class={cn("w-full bg-canvas", height)}
		sandbox="allow-scripts"
	></iframe>
</div>
