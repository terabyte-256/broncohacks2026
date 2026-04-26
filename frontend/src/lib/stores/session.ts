import { writable } from 'svelte/store';
import type { Session, User } from '@supabase/supabase-js';

export interface SessionUser {
	id: string;
	displayName: string;
	avatarUrl?: string;
	email?: string;
}

// Current authenticated session
export const session = writable<Session | null>(null);

// Current authenticated user
export const user = writable<User | null>(null);

// Derived user profile data for easy access
export const userProfile = writable<SessionUser | null>(null);

// Helper to update profile from User data
export function updateUserProfile(u: User | null) {
	if (!u) {
		userProfile.set(null);
		return;
	}
	
	userProfile.set({
		id: u.id,
		displayName: u.user_metadata?.full_name || u.user_metadata?.name || u.email?.split('@')[0] || 'User',
		avatarUrl: u.user_metadata?.avatar_url,
		email: u.email
	});
}
