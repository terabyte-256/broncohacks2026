import { env } from '$env/dynamic/private';
import type { Cookies } from '@sveltejs/kit';

export function createClient(cookies: Cookies) {
	return {
		auth: {
			signOut: async () => {
				return { data: null, error: null };
			}
		}
	};
}
