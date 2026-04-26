import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
	// Session is managed by the backend (Google OAuth)
	// Each request can check /auth/user endpoint to get the current user
	
	// Convenience helper for getting session
	event.locals.safeGetSession = async () => {
		try {
			const res = await fetch('http://127.0.0.1:5000/auth/user', {
				headers: {
					'Cookie': event.request.headers.get('cookie') || ''
				}
			});
			
			if (res.ok) {
				const user = await res.json();
				return { session: { user }, user };
			}
		} catch (error) {
			// Session not available
		}
		
		return { session: null, user: null };
	};

	return resolve(event);
};
