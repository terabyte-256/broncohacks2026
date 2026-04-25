<script lang="ts">
import { onMount } from 'svelte';
import { page } from '$app/state';
import { Alert, Badge, Button, Card, ProgressBar, QuizOption, SectionHeader } from '$lib/components';
import { getErrorMessage, getQuiz, submitQuiz, type Quiz, type QuizSubmissionResult } from '$lib/services';
import { createAsyncState } from '$lib/stores';

const quizState = createAsyncState<Quiz>();
const submissionState = createAsyncState<QuizSubmissionResult>();

let currentQuestionIndex = $state(0);
let selectedAnswers = $state<Record<number, number>>({});
let immediateFeedback = $state('');
let submitting = $state(false);

const currentQuestion = $derived.by(() => {
const quiz = $quizState.data;
if (!quiz) {
return null;
}
return quiz.questions[currentQuestionIndex] ?? null;
});

const answeredCount = $derived.by(() => Object.keys(selectedAnswers).length);
const totalQuestions = $derived.by(() => $quizState.data?.questions.length ?? 0);

function getQuizId(): number | null {
const value = Number.parseInt(page.params.id || '', 10);
if (!Number.isFinite(value) || value <= 0) {
return null;
}
return value;
}

function currentOptionId(): number | null {
const question = currentQuestion;
if (!question) {
return null;
}
const optionId = selectedAnswers[question.id];
return typeof optionId === 'number' ? optionId : null;
}

function updateImmediateFeedback(questionId: number, optionId: number): void {
const question = $quizState.data?.questions.find((entry) => entry.id === questionId);
const option = question?.options.find((entry) => entry.id === optionId);
if (!option) {
immediateFeedback = 'Answer saved.';
return;
}
immediateFeedback = `Saved answer ${option.label}. ${option.text}`;
}

async function loadQuiz() {
selectedAnswers = {};
currentQuestionIndex = 0;
immediateFeedback = '';
submissionState.reset();
quizState.setLoading();

const quizId = getQuizId();
if (quizId === null) {
quizState.setError('Invalid quiz id.');
return;
}

try {
const response = await getQuiz(quizId);
const sortedQuestions = [...response.quiz.questions].sort((a, b) => a.orderIndex - b.orderIndex);
if (!sortedQuestions.length) {
quizState.setEmpty('This quiz has no questions yet.');
return;
}
quizState.setSuccess({ ...response.quiz, questions: sortedQuestions });
} catch (error) {
quizState.setError(getErrorMessage(error));
}
}

function selectOption(optionId: number): void {
const question = currentQuestion;
if (!question || submitting || $submissionState.status === 'success') {
return;
}

selectedAnswers = {
...selectedAnswers,
[question.id]: optionId
};
updateImmediateFeedback(question.id, optionId);

if ($submissionState.status === 'error') {
submissionState.reset();
}
}

function goToPreviousQuestion(): void {
if (currentQuestionIndex <= 0) {
return;
}
currentQuestionIndex -= 1;
const question = currentQuestion;
if (!question) {
immediateFeedback = '';
return;
}
const optionId = selectedAnswers[question.id];
if (typeof optionId === 'number') {
updateImmediateFeedback(question.id, optionId);
} else {
immediateFeedback = '';
}
}

function goToNextQuestion(): void {
if (currentQuestionIndex >= totalQuestions - 1) {
return;
}
currentQuestionIndex += 1;
const question = currentQuestion;
if (!question) {
immediateFeedback = '';
return;
}
const optionId = selectedAnswers[question.id];
if (typeof optionId === 'number') {
updateImmediateFeedback(question.id, optionId);
} else {
immediateFeedback = '';
}
}

async function submitAnswers() {
if (submitting || !$quizState.data) {
return;
}

const unansweredQuestion = $quizState.data.questions.find((question) => selectedAnswers[question.id] === undefined);
if (unansweredQuestion) {
submissionState.setError('Please answer every question before submitting.');
return;
}

submitting = true;
submissionState.setLoading();

try {
const response = await submitQuiz($quizState.data.id, {
answers: $quizState.data.questions.map((question) => ({
questionId: question.id,
optionId: selectedAnswers[question.id]
}))
});
submissionState.setSuccess(response.result);
} catch (error) {
submissionState.setError(getErrorMessage(error));
} finally {
submitting = false;
}
}

const resultExplanation = $derived.by(() => {
const result = $submissionState.data;
const quiz = $quizState.data;
if (!result || !quiz) {
return '';
}
if (result.passed) {
return `You passed ${quiz.moduleTitle}. Keep applying the same phishing-detection habits.`;
}
return `Review ${quiz.moduleTitle} (${quiz.description}) and retry to improve your score.`;
});

onMount(() => {
void loadQuiz();
});
</script>

<SectionHeader title="Quiz" subtitle="One question at a time with backend submission on completion.">
{#snippet actions()}
<Button variant="secondary" onclick={loadQuiz}>Restart quiz</Button>
{/snippet}
</SectionHeader>

{#if $quizState.status === 'loading'}
<Card>
<p class="text-sm text-text-muted">Loading quiz...</p>
</Card>
{:else if $quizState.status === 'error'}
<Card>
<Alert variant="danger" title="Quiz failed to load">{$quizState.message}</Alert>
</Card>
{:else if $quizState.status === 'empty'}
<Card>
<Alert variant="warning">{$quizState.message}</Alert>
</Card>
{:else if $quizState.status === 'success' && $quizState.data && currentQuestion}
<div class="space-y-4">
<Card title={$quizState.data.title} description={$quizState.data.description}>
<div class="space-y-4">
<div class="space-y-2">
<div class="flex items-center justify-between gap-2 text-sm">
<p class="text-text-muted">
Question {currentQuestionIndex + 1} of {totalQuestions}
</p>
<p class="text-text-muted">Answered {answeredCount}/{totalQuestions}</p>
</div>
<ProgressBar value={((currentQuestionIndex + 1) / totalQuestions) * 100} label="Quiz progress" showValue={false} />
</div>

<div>
<p class="text-sm font-medium text-text">{currentQuestion.prompt}</p>
<fieldset class="mt-3 space-y-3">
<legend class="sr-only">Choose one answer option</legend>
{#each currentQuestion.options as option (option.id)}
<QuizOption
value={option.id}
label={option.label}
description={option.text}
selected={currentOptionId() === option.id}
disabled={submitting || $submissionState.status === 'success'}
on:select={() => selectOption(option.id)}
/>
{/each}
</fieldset>
</div>

{#if immediateFeedback}
<div aria-live="polite">
<Alert variant="info" title="Immediate feedback">{immediateFeedback}</Alert>
</div>
{/if}

<div class="flex flex-wrap gap-2">
<Button variant="secondary" onclick={goToPreviousQuestion} disabled={currentQuestionIndex === 0 || submitting}>
Previous
</Button>
<Button
variant="secondary"
onclick={goToNextQuestion}
disabled={
currentQuestionIndex >= totalQuestions - 1 ||
currentOptionId() === null ||
submitting ||
$submissionState.status === 'success'
}
>
Next question
</Button>
<Button
onclick={submitAnswers}
disabled={answeredCount !== totalQuestions || submitting || $submissionState.status === 'success'}
loading={submitting}
>
Submit quiz
</Button>
</div>
</div>
</Card>

{#if $submissionState.status === 'loading'}
<Alert variant="info">Submitting quiz answers...</Alert>
{:else if $submissionState.status === 'error'}
<Alert variant="danger" title="Could not submit answers">{$submissionState.message}</Alert>
{:else if $submissionState.status === 'success' && $submissionState.data}
<Card>
<div class="flex flex-wrap items-center gap-2">
<Badge variant={$submissionState.data.passed ? 'success' : 'warning'}>
{$submissionState.data.passed ? 'Passed' : 'Not passed'}
</Badge>
<p class="text-sm text-text-muted">Attempt #{$submissionState.data.attemptId}</p>
</div>
<p class="mt-3 text-sm text-text">
Score: {$submissionState.data.score}% ({$submissionState.data.correctAnswers}/{$submissionState.data.totalQuestions} correct)
</p>
<p class="mt-2 text-sm text-text-muted">{resultExplanation}</p>
</Card>
{/if}
</div>
{/if}
