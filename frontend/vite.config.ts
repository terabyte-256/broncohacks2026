import { defineConfig } from 'vitest/config';
import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
const env = loadEnv(mode, process.cwd(), '');
const backendDevOrigin = env.BACKEND_DEV_ORIGIN ?? 'http://127.0.0.1:5000';

// Map NEXT_PUBLIC_* to PUBLIC_* for SvelteKit compatibility
const supabaseUrl = env.PUBLIC_SUPABASE_URL || env.NEXT_PUBLIC_SUPABASE_URL || env.SUPABASE_URL;
const supabaseAnonKey = env.PUBLIC_SUPABASE_ANON_KEY || env.NEXT_PUBLIC_SUPABASE_ANON_KEY || env.SUPABASE_ANON_KEY;
const devSupabaseRedirectUrl = env.PUBLIC_DEV_SUPABASE_REDIRECT_URL || env.NEXT_PUBLIC_DEV_SUPABASE_REDIRECT_URL;

return {
plugins: [tailwindcss(), sveltekit()],
define: {
// Expose Supabase env vars to the client with PUBLIC_ prefix for SvelteKit
'import.meta.env.PUBLIC_SUPABASE_URL': JSON.stringify(supabaseUrl),
'import.meta.env.PUBLIC_SUPABASE_ANON_KEY': JSON.stringify(supabaseAnonKey),
'import.meta.env.PUBLIC_DEV_SUPABASE_REDIRECT_URL': JSON.stringify(devSupabaseRedirectUrl)
},
server: {
proxy: {
'/api': {
target: backendDevOrigin,
changeOrigin: true
}
}
},
test: {
expect: { requireAssertions: true },
projects: [
{
extends: './vite.config.ts',
test: {
name: 'server',
environment: 'node',
include: ['src/**/*.{test,spec}.{js,ts}'],
exclude: ['src/**/*.svelte.{test,spec}.{js,ts}']
}
}
]
}
};
});
