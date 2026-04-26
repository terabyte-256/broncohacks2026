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

	const TRACK_ID = 1;

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
		"phishing": {
			icon: "🎣",
			what: "Phishing attacks use fake emails, texts, or websites designed to look legitimate so you hand over credentials, click malicious links, or install malware. Attackers often impersonate trusted brands and create urgency to bypass your better judgment.",
			risk: "Phishing is the #1 cause of data breaches worldwide. A single click on a bad link can expose your login credentials, install ransomware, or give an attacker full access to your accounts — sometimes without you ever knowing.",
			example: "You receive an email from 'support@paypa1.com' — note the '1' instead of 'l' — marked URGENT saying your account will be suspended. The link leads to a pixel-perfect fake login page that captures your password the moment you type it.",
			tips: [
				"Check the sender's domain carefully — paypa1.com is not paypal.com",
				"Slow down when you feel urgency — 'act within 24 hours' is a manipulation tactic",
				"Hover over any link to preview where it actually goes before clicking",
				"When in doubt, open a new tab and navigate to the site yourself by typing the URL",
				"Enable MFA so stolen passwords alone can't get attackers in",
			],
		},
		"social-engineering": {
			icon: "🧠",
			what: "Social engineering is the art of manipulating people — not computers — into giving up confidential information or taking unsafe actions. Attackers exploit trust, authority, fear, and helpfulness to bypass technical defenses entirely.",
			risk: "No firewall can stop a human from being tricked. Social engineering is behind the majority of corporate breaches because it's far easier to deceive a person than to crack a well-secured system. Everyone is a potential target.",
			example: "You receive a phone call: 'Hi, this is Alex from IT — we've detected a virus on your account and need your login credentials right now to fix it before you lose all your files.' The urgency and authority feel real, but it's an attacker.",
			tips: [
				"Legitimate IT teams will never ask for your password — refuse any request for credentials",
				"Verify the identity of anyone making unusual requests through a separate, known-good channel",
				"Be suspicious of extreme urgency or requests to keep something secret",
				"Think before you act — social engineers rely on you reacting without thinking",
				"When something feels off, it probably is — trust your instincts and slow down",
			],
		},
		"auth-passwords": {
			icon: "🔐",
			what: "Authentication security means using strong, unique passwords combined with multi-factor authentication (MFA). A password manager handles the complexity for you — generating and storing a different strong password for every site so you never need to reuse one.",
			risk: "Credential stuffing tools automatically test billions of leaked username/password pairs across hundreds of sites per minute. If you reuse passwords, one breach cascades into all your accounts. MFA stops this even when passwords are already stolen.",
			example: "Your email password from a 2021 breach surfaces in a dark web dump. Within hours an automated tool tests it against your bank, social media, and work accounts — logging into three of them because you reused the same password.",
			tips: [
				"Use a password manager (Bitwarden, 1Password) to generate and store unique passwords for every site",
				"A strong password is at least 16 characters and completely random — let the manager create it",
				"Enable MFA on every account, especially email, banking, and work — use an authenticator app over SMS",
				"Never reuse passwords and never share them via email, chat, or text",
				"Change passwords immediately whenever you get a breach notification",
			],
		},
		"sessions": {
			icon: "🍪",
			what: "After you log in, a website gives your browser a session token (stored as a cookie) to keep you authenticated. That token is your digital key — if an attacker gets hold of it, they can access your account without ever knowing your password.",
			risk: "Session hijacking lets attackers impersonate you completely — bypassing passwords and MFA entirely — by stealing the token your browser holds. This can happen over unsecured networks, through malicious scripts, or on shared computers where sessions were left open.",
			example: "You check your bank on a public café Wi-Fi without HTTPS. An attacker on the same network intercepts your session cookie using a simple sniffing tool. They now have full access to your bank account without needing your username or password.",
			tips: [
				"Always log out on shared or public computers — closing a tab does not end your session",
				"Only use sites over HTTPS (the padlock icon) especially for anything sensitive",
				"Avoid accessing sensitive accounts on public Wi-Fi — use a VPN if you must",
				"Check for 'active sessions' in account settings and revoke any you don't recognize",
				"Keep your browser and OS updated — patches often fix session-stealing vulnerabilities",
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
			subtitle="Beginner Track · Read the lesson, then take the quiz"
		>
			{#snippet actions()}
				<Button variant="secondary" href="/">← Home</Button>
				<Button
					variant="secondary"
					href="/tracks/beginner"
					>← Back to categories</Button
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
		title={$quizState.data?.title ?? "Quiz"}
		subtitle="Answer every question, then submit."
	>
		{#snippet actions()}
			<Button variant="secondary" href="/">← Home</Button>
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
			<Button variant="secondary" href="/">← Home</Button>
			<Button variant="secondary" onclick={restartQuiz}
				>↺ Retake quiz</Button
			>
			<Button href="/tracks/beginner">Back to categories</Button>
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
			<Button href="/tracks/beginner"
				>Continue to next module →</Button
			>
		</div>
	</div>
{/if}
