export interface DashboardMetrics {
totalTracks: number;
completedTracks: number;
totalModules: number;
completedModules: number;
averageQuizScore: number;
streakDays: number;
}

export interface RecentQuizAttempt {
id: number;
quizId: number;
quizTitle: string;
score: number;
submittedAt: string;
}

export interface TrackSummary {
id: number;
title: string;
description: string;
moduleCount: number;
completedModules: number;
completionPercent: number;
}

export interface DashboardData {
metrics: DashboardMetrics;
recentQuizAttempts: RecentQuizAttempt[];
trackProgress: TrackSummary[];
}

export interface TracksResponse {
tracks: TrackSummary[];
}

export interface TrackInfo {
id: number;
title: string;
description: string;
}

export interface TrackModule {
id: number;
trackId: number;
title: string;
description: string;
topicKey: string;
orderIndex: number;
completionPercent: number;
lastScore: number | null;
completed: boolean;
quizId: number | null;
}

export interface TrackModulesResponse {
track: TrackInfo;
modules: TrackModule[];
}

export interface QuizAnswerOption {
id: number;
label: string;
text: string;
}

export interface QuizQuestion {
id: number;
prompt: string;
orderIndex: number;
options: QuizAnswerOption[];
}

export interface Quiz {
id: number;
moduleId: number;
title: string;
description: string;
moduleTitle: string;
questions: QuizQuestion[];
}

export interface QuizResponse {
quiz: Quiz;
}

export interface QuizAnswer {
questionId: number;
optionId: number;
}

export interface QuizSubmissionRequest {
answers: QuizAnswer[];
}

export interface QuizSubmissionResult {
attemptId: number;
score: number;
correctAnswers: number;
totalQuestions: number;
passed: boolean;
}

export interface QuizSubmissionResponse {
result: QuizSubmissionResult;
}

export interface ProgressSummary {
totalModules: number;
completedModules: number;
averageCompletionPercent: number;
}

export interface ProgressModule {
moduleId: number;
trackId: number;
title: string;
completionPercent: number;
lastScore: number | null;
lastUpdatedAt: string | null;
completed: boolean;
}

export interface ProgressData {
summary: ProgressSummary;
modules: ProgressModule[];
}

export interface ProgressUpdateRequest {
moduleId: number;
completionPercent: number;
lastScore?: number;
}

export interface ProgressUpdateResponse {
progress: ProgressModule;
}

export interface AnalyzeMessageRequest {
message: string;
}

export type RiskLevel = 'Low' | 'Medium' | 'High';

export interface MessageAnalysis {
verdict: string;
riskLevel: RiskLevel;
redFlags: string[];
explanation: string;
tips: string[];
}

export interface MessageHistoryItem {
id: number;
message: string;
verdict: string;
riskLevel: RiskLevel;
redFlags: string[];
explanation: string;
tips: string[];
createdAt: string;
}

export interface MessageHistoryResponse {
history: MessageHistoryItem[];
}
