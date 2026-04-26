import { env } from '$env/dynamic/public';

let supabaseClient: any = null;

export function createClient() {
	if (supabaseClient) {
		return supabaseClient;
	}
	
	// Stub client for backward compatibility
	// The actual authentication is handled by the backend
	supabaseClient = {
		auth: {
			signOut: async () => {
				return { data: null, error: null };
			},
			onAuthStateChange: (_callback: unknown) => {
				return { data: { subscription: { unsubscribe: () => {} } } };
			}
		}
	};
	
	return supabaseClient;
}
