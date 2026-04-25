<script lang="ts">
	import { onMount } from 'svelte';
	import { invalidate } from '$app/navigation';
	import { createClient } from '$lib/supabase/client';
	import { session, user, updateUserProfile } from '$lib/stores/session';
	import "./layout.css";
	import favicon from "$lib/assets/favicon.svg";
	import { AppShell } from "$lib/layouts";

	let { data, children } = $props();

	// Initialize stores with server data
	$effect(() => {
		session.set(data.session);
		user.set(data.user);
		updateUserProfile(data.user);
	});

	onMount(() => {
		const supabase = createClient();

		// Listen for auth state changes
		const { data: { subscription } } = supabase.auth.onAuthStateChange((_, newSession) => {
			if (newSession?.expires_at !== data.session?.expires_at) {
				invalidate('supabase:auth');
			}
		});

		return () => subscription.unsubscribe();
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>CyberLearn</title>
</svelte:head>

<AppShell user={data.user}>
	{@render children()}
</AppShell>
