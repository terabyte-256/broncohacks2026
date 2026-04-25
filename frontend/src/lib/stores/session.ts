import { writable } from 'svelte/store';

export interface SessionUser {
id: string;
displayName: string;
}

export const defaultUser = writable<SessionUser>({
id: 'default-user',
displayName: 'CyberLearner User'
});
