<script lang="ts">
import { cn } from '$lib/theme';
import { onMount } from 'svelte';
import { createSandboxHTML } from '$lib/sandbox-utils';

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
let alertMessage: string | null = null;
let alertVisible = false;

function renderSandbox() {
if (!iframeRef) return;
const sandboxContent = createSandboxHTML(html);
const blob = new Blob([sandboxContent], { type: 'text/html' });
const url = URL.createObjectURL(blob);
if (iframeRef.src && iframeRef.src.startsWith('blob:')) {
URL.revokeObjectURL(iframeRef.src);
}
iframeRef.src = url;
}

function handleMessage(event: MessageEvent) {
if (event.data?.type === 'sandbox-alert') {
alertMessage = event.data.message;
alertVisible = true;
onAlert?.(event.data.message);
setTimeout(() => {
alertVisible = false;
}, 3000);
}
}

onMount(() => {
window.addEventListener('message', handleMessage);
renderSandbox();
return () => window.removeEventListener('message', handleMessage);
});

$effect(() => {
if (html) {
renderSandbox();
}
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
