import { env as publicEnv } from '$env/dynamic/public';

import type {
AnalyzeMessageRequest,
DashboardData,
MessageAnalysis,
MessageHistoryResponse,
ProgressData,
ProgressUpdateRequest,
ProgressUpdateResponse,
QuizResponse,
QuizSubmissionRequest,
QuizSubmissionResponse,
TrackModulesResponse,
TracksResponse
} from './types';

const DEFAULT_API_BASE = '/api';
const API_BASE = normalizeApiBase(publicEnv.PUBLIC_API_BASE);

export class ApiError extends Error {
status: number;
details: unknown;

constructor(message: string, status: number, details?: unknown) {
super(message);
this.name = 'ApiError';
this.status = status;
this.details = details;
}
}

interface RequestOptions {
fetchFn?: typeof fetch;
method?: 'GET' | 'POST';
body?: unknown;
signal?: AbortSignal;
}

function normalizeApiBase(apiBase: string | undefined): string {
const candidate = apiBase?.trim();
if (!candidate) {
return DEFAULT_API_BASE;
}

return candidate.replace(/\/+$/, '');
}

function parseBody(body: string): unknown {
if (!body) {
return null;
}

try {
return JSON.parse(body);
} catch {
return body;
}
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
const fetchFn = options.fetchFn ?? fetch;
const response = await fetchFn(`${API_BASE}${path}`, {
method: options.method ?? 'GET',
headers: {
'Content-Type': 'application/json'
},
body: options.body ? JSON.stringify(options.body) : undefined,
signal: options.signal
});

const rawBody = await response.text();
const parsed = parseBody(rawBody);

if (!response.ok) {
const message = typeof parsed === 'object' && parsed && 'message' in parsed ? String(parsed.message) : 'Request failed';
throw new ApiError(message, response.status, parsed);
}

return parsed as T;
}

export async function getDashboard(fetchFn?: typeof fetch): Promise<DashboardData> {
return request<DashboardData>('/dashboard', { fetchFn });
}

export async function getTracks(fetchFn?: typeof fetch): Promise<TracksResponse> {
return request<TracksResponse>('/tracks', { fetchFn });
}

export async function getTrackModules(trackId: number, fetchFn?: typeof fetch): Promise<TrackModulesResponse> {
return request<TrackModulesResponse>(`/tracks/${trackId}/modules`, { fetchFn });
}

export async function getQuiz(quizId: number, fetchFn?: typeof fetch): Promise<QuizResponse> {
return request<QuizResponse>(`/quizzes/${quizId}`, { fetchFn });
}

export async function submitQuiz(
quizId: number,
payload: QuizSubmissionRequest,
fetchFn?: typeof fetch
): Promise<QuizSubmissionResponse> {
return request<QuizSubmissionResponse>(`/quizzes/${quizId}/submit`, {
fetchFn,
method: 'POST',
body: payload
});
}

export async function getProgress(fetchFn?: typeof fetch): Promise<ProgressData> {
return request<ProgressData>('/progress', { fetchFn });
}

export async function postProgress(
payload: ProgressUpdateRequest,
fetchFn?: typeof fetch
): Promise<ProgressUpdateResponse> {
return request<ProgressUpdateResponse>('/progress', {
fetchFn,
method: 'POST',
body: payload
});
}

export async function analyzeMessage(
payload: AnalyzeMessageRequest,
fetchFn?: typeof fetch
): Promise<MessageAnalysis> {
return request<MessageAnalysis>('/analyze-message', {
fetchFn,
method: 'POST',
body: payload
});
}

export async function getMessageHistory(limit?: number, fetchFn?: typeof fetch): Promise<MessageHistoryResponse> {
const query = typeof limit === 'number' ? `?limit=${limit}` : '';
return request<MessageHistoryResponse>(`/message-history${query}`, { fetchFn });
}

export function getErrorMessage(error: unknown): string {
if (error instanceof ApiError) {
return `${error.message} (status ${error.status})`;
}

if (error instanceof Error) {
return error.message;
}

return 'Unexpected error';
}
