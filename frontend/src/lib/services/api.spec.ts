import { describe, expect, it } from 'vitest';
import { ApiError, getDashboard, getMessageHistory, submitQuiz } from './api';

describe('api service', () => {
it('parses successful JSON responses', async () => {
const data = {
metrics: {
totalTracks: 4,
completedTracks: 1,
totalModules: 8,
completedModules: 3,
averageQuizScore: 82,
streakDays: 2
},
recentQuizAttempts: [],
trackProgress: []
};
const fetchFn: typeof fetch = async () =>
new Response(JSON.stringify(data), {
status: 200,
headers: { 'Content-Type': 'application/json' }
});

await expect(getDashboard(fetchFn)).resolves.toEqual(data);
});

it('throws ApiError for non-2xx responses', async () => {
const fetchFn: typeof fetch = async () =>
new Response(JSON.stringify({ message: 'Bad request' }), {
status: 400,
headers: { 'Content-Type': 'application/json' }
});

await expect(getDashboard(fetchFn)).rejects.toBeInstanceOf(ApiError);
});

it('posts quiz answers as expected', async () => {
const payload = { answers: [{ questionId: 1, optionId: 2 }] };
const fetchFn: typeof fetch = async (_, init) => {
expect(init?.method).toBe('POST');
expect(init?.body).toBe(JSON.stringify(payload));
return new Response(JSON.stringify({ result: { attemptId: 12, score: 100, correctAnswers: 1, totalQuestions: 1, passed: true } }), {
status: 200,
headers: { 'Content-Type': 'application/json' }
});
};

await expect(submitQuiz(2, payload, fetchFn)).resolves.toEqual({
result: { attemptId: 12, score: 100, correctAnswers: 1, totalQuestions: 1, passed: true }
});
});

it('supports optional history limit query', async () => {
const fetchFn: typeof fetch = async (input) => {
expect(String(input)).toContain('/api/message-history?limit=10');
return new Response(JSON.stringify({ history: [] }), {
status: 200,
headers: { 'Content-Type': 'application/json' }
});
};

await expect(getMessageHistory(10, fetchFn)).resolves.toEqual({ history: [] });
});
});
