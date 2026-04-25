import { createBrowserClient } from '@supabase/ssr';
import { env } from '$env/dynamic/public';

let supabaseClient: ReturnType<typeof createBrowserClient> | null = null;

export function createClient() {
	if (supabaseClient) {
		return supabaseClient;
	}
	
	// Try multiple env var naming patterns
	const supabaseUrl = env.PUBLIC_SUPABASE_URL;
	const supabaseAnonKey = env.PUBLIC_SUPABASE_ANON_KEY;
	
	if (!supabaseUrl || !supabaseAnonKey) {
		throw new Error('Missing Supabase environment variables. Please ensure PUBLIC_SUPABASE_URL and PUBLIC_SUPABASE_ANON_KEY are set.');
	}
	
	supabaseClient = createBrowserClient(supabaseUrl, supabaseAnonKey);
	return supabaseClient;
}
