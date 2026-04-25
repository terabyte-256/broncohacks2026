import { writable } from 'svelte/store';

export type AsyncStatus = 'idle' | 'loading' | 'success' | 'empty' | 'error';

export interface AsyncState<T> {
status: AsyncStatus;
data: T | null;
message: string | null;
}

export function createAsyncState<T>(initialData: T | null = null) {
const { subscribe, set } = writable<AsyncState<T>>({
status: initialData ? 'success' : 'idle',
data: initialData,
message: null
});

return {
subscribe,
setLoading() {
set({ status: 'loading', data: null, message: null });
},
setSuccess(data: T, message: string | null = null) {
set({ status: 'success', data, message });
},
setEmpty(message = 'No data found.') {
set({ status: 'empty', data: null, message });
},
setError(message: string) {
set({ status: 'error', data: null, message });
},
reset() {
set({ status: 'idle', data: initialData, message: null });
}
};
}
