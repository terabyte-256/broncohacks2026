<script lang="ts">
import './layout.css';
import favicon from '$lib/assets/favicon.svg';
import { AppShell } from '$lib/layouts';

let { children } = $props();
</script>

<svelte:head>
<link rel="icon" href={favicon} />
<title>CyberLearn</title>
</svelte:head>

<AppShell>
{@render children()}
</AppShell>
