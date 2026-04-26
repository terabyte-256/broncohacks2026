<script lang="ts">
	import { onMount } from "svelte";
	import { page } from "$app/state";
	import {
		Alert,
		Badge,
		Button,
		Card,
		ProgressBar,
		QuizOption,
		SectionHeader,
	} from "$lib/components";
	import {
		getErrorMessage,
		getQuiz,
		getTrackModules,
		postProgress,
		submitQuiz,
		type Quiz,
		type QuizSubmissionResult,
		type TrackModule,
	} from "$lib/services";
	import { createAsyncState } from "$lib/stores";

	const TRACK_ID = 3;

	type View = "intro" | "quiz" | "result";
	let view = $state<View>("intro");

	const moduleState = createAsyncState<TrackModule>();
	const quizState = createAsyncState<Quiz>();
	const submissionState = createAsyncState<QuizSubmissionResult>();

	let currentQuestionIndex = $state(0);
	let selectedAnswers = $state<Record<number, number>>({});
	let immediateFeedback = $state("");
	let submitting = $state(false);

	const currentQuestion = $derived.by(() => {
		const quiz = $quizState.data;
		if (!quiz) return null;
		return quiz.questions[currentQuestionIndex] ?? null;
	});

	const answeredCount = $derived.by(
		() => Object.keys(selectedAnswers).length,
	);
	const totalQuestions = $derived.by(
		() => $quizState.data?.questions.length ?? 0,
	);

	function currentOptionId(): number | null {
		const question = currentQuestion;
		if (!question) return null;
		const optionId = selectedAnswers[question.id];
		return typeof optionId === "number" ? optionId : null;
	}

	function updateImmediateFeedback(
		questionId: number,
		optionId: number,
	): void {
		const question = $quizState.data?.questions.find(
			(q) => q.id === questionId,
		);
		const option = question?.options.find((o) => o.id === optionId);
		if (!option) {
			immediateFeedback = "Answer saved.";
			return;
		}
		immediateFeedback = `Saved answer ${option.label}. ${option.text}`;
	}

	// ── Lesson content keyed to topic_key values from seed ──
	const LESSON_CONTENT: Record<
		string,
		{
			icon: string;
			what: string;
			risk: string;
			example: string;
			tips: string[];
		}
	> = {
		"xss": {
			icon: "💉",
			what: "Cross-Site Scripting (XSS) is a vulnerability where an attacker injects malicious scripts into web pages viewed by other users. Because the script runs in the victim's browser with the trust of the legitimate site, it can read cookies, hijack sessions, or rewrite page content — all without the victim realizing anything is wrong.",
			risk: "XSS is one of the most prevalent web vulnerabilities. A successful attack can steal session tokens to fully impersonate a user, capture keystrokes including passwords, redirect users to phishing pages, or silently perform actions on their behalf — all from a single unsanitized input field.",
			example: "A blog allows users to post comments without sanitizing input. An attacker submits a comment containing a script tag that exfiltrates document.cookie to an external server. Every visitor who loads that page silently sends their session cookie to the attacker, who can then log in as them instantly.",
			tips: [
				"Always escape and encode user-supplied data before rendering it in HTML, JS, or CSS contexts",
				"Use a Content Security Policy (CSP) header to restrict which scripts the browser will execute",
				"Prefer framework template engines (React, Svelte, Vue) that escape output by default",
				"Never use innerHTML, document.write, or eval with user-controlled data",
				"Set the HttpOnly flag on session cookies so JavaScript cannot read them even if XSS occurs",
			],
		},
		"sql-injection": {
			icon: "🗄️",
			what: "SQL Injection occurs when user-supplied input is embedded directly into a database query without proper sanitization, allowing an attacker to alter the query's logic. Instead of data, the attacker sends SQL syntax — changing what the query does, what it returns, or even which tables it touches.",
			risk: "A successful SQL injection can bypass authentication entirely, expose every record in a database, modify or delete data, and in some configurations execute operating system commands on the database server. A single vulnerable login form can hand an attacker the entire user table.",
			example: "A login form builds its query by concatenating user input directly into a SQL string. An attacker enters a specially crafted username containing OR '1'='1. The resulting query always evaluates to true, granting access without a valid password — or they append a DROP TABLE statement to destroy data entirely.",
			tips: [
				"Always use parameterized queries or prepared statements — never concatenate user input into SQL strings",
				"Use an ORM (SQLAlchemy, Prisma, Hibernate) that parameterizes queries by default",
				"Apply the principle of least privilege — the database user your app connects with should only have the permissions it needs",
				"Validate and allowlist input types before they reach the database layer",
				"Never display raw database error messages to users — they reveal table and column names to attackers",
			],
		},
		"csrf": {
			icon: "🎭",
			what: "Cross-Site Request Forgery (CSRF) tricks an authenticated user's browser into sending an unwanted request to a site where they're already logged in. Because the browser automatically attaches cookies, the target server sees a legitimate-looking request — even though the user never intended to make it.",
			risk: "CSRF can force authenticated users to change their email address, transfer funds, reset passwords, or delete their account — all without their knowledge. Any state-changing action exposed via a GET or unprotected POST endpoint is potentially exploitable, even with HTTPS.",
			example: "A user is logged into their bank. They then visit a malicious page containing an image tag whose src points to the bank's fund-transfer endpoint with attacker-controlled parameters. The browser fires that request automatically with the user's session cookie attached, and the transfer goes through silently.",
			tips: [
				"Use CSRF tokens — unique, secret, per-session values embedded in forms and verified server-side on every state-changing request",
				"Check the Origin and Referer headers to ensure requests come from your own domain",
				"Use the SameSite=Strict or SameSite=Lax cookie attribute to prevent cookies from being sent on cross-origin requests",
				"Never use GET requests for state-changing actions — use POST, PUT, PATCH, or DELETE",
				"Modern frameworks (Django, Rails, Laravel) include CSRF protection by default — make sure it's enabled and not accidentally disabled",
			],
		},
	};

	function getLessonContent(module: TrackModule) {
		return (
			LESSON_CONTENT[module.topicKey] ?? {
				icon: "📘",
				what: module.description,
				risk: "Understanding this topic helps protect you from common cyber threats.",
				example: "Review the quiz questions for real-world scenarios related to this topic.",
				tips: [
					"Stay alert",
					"Verify before you act",
					"When in doubt, don't click",
				],
			}
		);
	}

	async function loadModule() {
		moduleState.setLoading();
		const moduleId = Number.parseInt(
			page.params.ID || "",
			10,
		);
		if (!Number.isFinite(moduleId) || moduleId <= 0) {
			moduleState.setError("Invalid module.");
			return;
		}
		try {
			const response = await getTrackModules(TRACK_ID);
			const mod = response.modules.find(
				(m) => m.id === moduleId,
			);
			if (!mod) {
				moduleState.setError("Module not found.");
				return;
			}
			moduleState.setSuccess(mod);
		} catch (error) {
			moduleState.setError(getErrorMessage(error));
		}
	}

	async function startQuiz() {
		const mod = $moduleState.data;
		if (!mod?.quizId) {
			quizState.setError(
				"No quiz available for this module.",
			);
			view = "quiz";
			return;
		}
		selectedAnswers = {};
		currentQuestionIndex = 0;
		immediateFeedback = "";
		submissionState.reset();
		quizState.setLoading();
		view = "quiz";

		try {
			const response = await getQuiz(mod.quizId);
			const sorted = [...response.quiz.questions].sort(
				(a, b) => a.orderIndex - b.orderIndex,
			);
			if (!sorted.length) {
				quizState.setEmpty(
					"This quiz has no questions yet.",
				);
				return;
			}
			quizState.setSuccess({
				...response.quiz,
				questions: sorted,
			});
		} catch (error) {
			quizState.setError(getErrorMessage(error));
		}
	}

	function selectOption(optionId: number): void {
		const question = currentQuestion;
		if (
			!question ||
			submitting ||
			$submissionState.status === "success"
		)
			return;
		selectedAnswers = {
			...selectedAnswers,
			[question.id]: optionId,
		};
		updateImmediateFeedback(question.id, optionId);
		if ($submissionState.status === "error")
			submissionState.reset();
	}

	function goToPreviousQuestion(): void {
		if (currentQuestionIndex <= 0) return;
		currentQuestionIndex -= 1;
		const question = currentQuestion;
		if (!question) {
			immediateFeedback = "";
			return;
		}
		const optionId = selectedAnswers[question.id];
		if (typeof optionId === "number")
			updateImmediateFeedback(question.id, optionId);
		else immediateFeedback = "";
	}

	function goToNextQuestion(): void {
		if (currentQuestionIndex >= totalQuestions - 1) return;
		currentQuestionIndex += 1;
		const question = currentQuestion;
		if (!question) {
			immediateFeedback = "";
			return;
		}
		const optionId = selectedAnswers[question.id];
		if (typeof optionId === "number")
			updateImmediateFeedback(question.id, optionId);
		else immediateFeedback = "";
	}

	async function submitAnswers() {
		if (submitting || !$quizState.data) return;
		const unanswered = $quizState.data.questions.find(
			(q) => selectedAnswers[q.id] === undefined,
		);
		if (unanswered) {
			submissionState.setError(
				"Please answer every question before submitting.",
			);
			return;
		}
		submitting = true;
		submissionState.setLoading();
		try {
			const response = await submitQuiz($quizState.data.id, {
				answers: $quizState.data.questions.map((q) => ({
					questionId: q.id,
					optionId: selectedAnswers[q.id],
				})),
			});
			submissionState.setSuccess(response.result);

			// Save progress — non-blocking
			const mod = $moduleState.data;
			if (mod) {
				await postProgress({
					moduleId: mod.id,
					completionPercent: 100,
					lastScore: response.result.score,
				}).catch(() => {});
			}
			view = "result";
		} catch (error) {
			submissionState.setError(getErrorMessage(error));
		} finally {
			submitting = false;
		}
	}

	function restartQuiz() {
		selectedAnswers = {};
		currentQuestionIndex = 0;
		immediateFeedback = "";
		submissionState.reset();
		quizState.reset();
		view = "intro";
	}

	const resultExplanation = $derived.by(() => {
		const result = $submissionState.data;
		const quiz = $quizState.data;
		if (!result || !quiz) return "";
		if (result.passed)
			return `You passed ${quiz.moduleTitle}. Keep applying these habits to stay protected.`;
		return `Review ${quiz.moduleTitle} (${quiz.description}) and retry to improve your score.`;
	});

	onMount(() => {
		void loadModule();
	});
</script>

<!-- ══ INTRO ══ -->
{#if view === "intro"}
	{#if $moduleState.status === "loading"}
		<SectionHeader title="Loading…" subtitle="" />
		<Card>
			<div class="space-y-3">
				<div
					class="h-4 w-48 animate-pulse rounded bg-muted"
				></div>
				<div
					class="h-3 w-full animate-pulse rounded bg-muted"
				></div>
				<div
					class="h-3 w-3/4 animate-pulse rounded bg-muted"
				></div>
			</div>
		</Card>
	{:else if $moduleState.status === "error"}
		<SectionHeader title="Module" subtitle="" />
		<Card>
			<Alert variant="danger" title="Could not load module"
				>{$moduleState.message}</Alert
			>
		</Card>
	{:else if $moduleState.status === "success" && $moduleState.data}
		{@const mod = $moduleState.data}
		{@const lesson = getLessonContent(mod)}

		<SectionHeader
			title={mod.title}
			subtitle="Developer Track · Learn real-world attack techniques and test your knowledge"
		>
			{#snippet actions()}
				<Button
					variant="secondary"
					href="/tracks/developer"
					>← Back to modules</Button
				>
			{/snippet}
		</SectionHeader>

		<div class="space-y-4">
			{#if mod.completed}
				<Alert
					variant="success"
					title="Module completed"
				>
					You previously scored {mod.lastScore}%
					on this module. You can retake the quiz
					anytime.
				</Alert>
			{/if}

			<Card>
				<p
					class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand-strong"
				>
					What is it?
				</p>
				<p class="text-sm text-text-muted">
					{lesson.what}
				</p>
			</Card>

			<Card>
				<p
					class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand-strong"
				>
					Why is it a risk?
				</p>
				<p class="text-sm text-text-muted">
					{lesson.risk}
				</p>
			</Card>

			<Card>
				<p
					class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand-strong"
				>
					Real-world example
				</p>
				<div
					class="rounded-lg border-l-4 border-warning-border bg-warning-soft px-4 py-3 text-sm text-text"
				>
					{lesson.example}
				</div>
			</Card>

			<Card>
				<p
					class="mb-3 text-xs font-semibold uppercase tracking-widest text-brand-strong"
				>
					How to stay safe
				</p>
				<ul class="space-y-2">
					{#each lesson.tips as tip}
						<li
							class="flex items-start gap-2 text-sm text-text-muted"
						>
							<span
								class="mt-0.5 font-bold text-success"
								>→</span
							>
							{tip}
						</li>
					{/each}
				</ul>
			</Card>

			<div class="flex justify-end">
				<Button
					onclick={startQuiz}
					disabled={!mod.quizId}
				>
					{mod.quizId
						? "Start Quiz →"
						: "No quiz available"}
				</Button>
			</div>
		</div>
	{/if}

	<!-- ══ QUIZ ══ -->
{:else if view === "quiz"}
	<SectionHeader
		title="Quiz"
		subtitle="One question at a time with backend submission on completion."
	>
		{#snippet actions()}
			<Button variant="secondary" onclick={restartQuiz}
				>← Back to lesson</Button
			>
		{/snippet}
	</SectionHeader>

	{#if $quizState.status === "loading"}
		<Card><p class="text-sm text-text-muted">Loading quiz…</p></Card
		>
	{:else if $quizState.status === "error"}
		<Card
			><Alert variant="danger" title="Quiz failed to load"
				>{$quizState.message}</Alert
			></Card
		>
	{:else if $quizState.status === "empty"}
		<Card
			><Alert variant="warning">{$quizState.message}</Alert
			></Card
		>
	{:else if $quizState.status === "success" && $quizState.data && currentQuestion}
		<div class="space-y-4">
			<Card
				title={$quizState.data.title}
				description={$quizState.data.description}
			>
				<div class="space-y-4">
					<div class="space-y-2">
						<div
							class="flex items-center justify-between gap-2 text-sm"
						>
							<p
								class="text-text-muted"
							>
								Question {currentQuestionIndex +
									1} of {totalQuestions}
							</p>
							<p
								class="text-text-muted"
							>
								Answered {answeredCount}/{totalQuestions}
							</p>
						</div>
						<ProgressBar
							value={((currentQuestionIndex +
								1) /
								totalQuestions) *
								100}
							label="Quiz progress"
							showValue={false}
						/>
					</div>

					<div>
						<p
							class="text-sm font-medium text-text"
						>
							{currentQuestion.prompt}
						</p>
						<fieldset
							class="mt-3 space-y-3"
						>
							<legend class="sr-only"
								>Choose one
								answer option</legend
							>
							{#each currentQuestion.options as option (option.id)}
								<QuizOption
									value={option.id}
									label={option.label}
									description={option.text}
									selected={currentOptionId() ===
										option.id}
									disabled={submitting ||
										$submissionState.status ===
											"success"}
									onselect={() =>
										selectOption(
											option.id,
										)}
								/>
							{/each}
						</fieldset>
					</div>

					{#if immediateFeedback}
						<div aria-live="polite">
							<Alert
								variant="info"
								title="Answer saved"
								>{immediateFeedback}</Alert
							>
						</div>
					{/if}

					<div class="flex flex-wrap gap-2">
						<Button
							variant="secondary"
							onclick={goToPreviousQuestion}
							disabled={currentQuestionIndex ===
								0 || submitting}
						>
							Previous
						</Button>
						<Button
							variant="secondary"
							onclick={goToNextQuestion}
							disabled={currentQuestionIndex >=
								totalQuestions -
									1 ||
								currentOptionId() ===
									null ||
								submitting ||
								$submissionState.status ===
									"success"}
						>
							Next question
						</Button>
						<Button
							onclick={submitAnswers}
							disabled={answeredCount !==
								totalQuestions ||
								submitting ||
								$submissionState.status ===
									"success"}
							loading={submitting}
						>
							Submit quiz
						</Button>
					</div>
				</div>
			</Card>

			{#if $submissionState.status === "loading"}
				<Alert variant="info"
					>Submitting quiz answers…</Alert
				>
			{:else if $submissionState.status === "error"}
				<Alert
					variant="danger"
					title="Could not submit answers"
					>{$submissionState.message}</Alert
				>
			{/if}
		</div>
	{/if}

	<!-- ══ RESULT ══ -->
{:else if view === "result" && $submissionState.data}
	<SectionHeader title="Quiz Complete" subtitle="Here's how you did.">
		{#snippet actions()}
			<Button variant="secondary" onclick={restartQuiz}
				>Retake quiz</Button
			>
			<Button href="/tracks/developer">Back to modules</Button>
		{/snippet}
	</SectionHeader>

	<div class="space-y-4">
		<Card>
			<div class="flex flex-wrap items-center gap-3">
				<Badge
					variant={$submissionState.data.passed
						? "success"
						: "warning"}
				>
					{$submissionState.data.passed
						? "Passed"
						: "Not passed"}
				</Badge>
				<p class="text-sm text-text-muted">
					Attempt #{$submissionState.data
						.attemptId}
				</p>
			</div>
			<p class="mt-4 text-3xl font-semibold text-text">
				{$submissionState.data.score}%
			</p>
			<p class="mt-1 text-sm text-text-muted">
				{$submissionState.data.correctAnswers} of {$submissionState
					.data.totalQuestions} correct
			</p>
			<div class="mt-4">
				<ProgressBar
					value={$submissionState.data.score}
					label="Quiz score"
				/>
			</div>
			<p class="mt-4 text-sm text-text-muted">
				{resultExplanation}
			</p>
		</Card>

		<div class="flex flex-wrap gap-3">
			<Button variant="secondary" onclick={restartQuiz}
				>↺ Retake quiz</Button
			>
			<Button href="/tracks/developer"
				>Continue to next module →</Button
			>
		</div>
	</div>
{/if}