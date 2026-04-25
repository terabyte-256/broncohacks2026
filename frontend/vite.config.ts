import { defineConfig } from 'vitest/config';
import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
const env = loadEnv(mode, process.cwd(), '');
const backendDevOrigin = env.BACKEND_DEV_ORIGIN ?? 'http://127.0.0.1:5000';

return {
plugins: [tailwindcss(), sveltekit()],
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
