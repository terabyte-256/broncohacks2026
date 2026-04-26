<script lang="ts">
	import { onMount } from 'svelte';
	import { Chart } from 'chart.js';
	import { browser } from '$app/environment';

	let totalUsers = $state(0);
	let totalQuizAttempts = $state(0);
	let averageScore = $state(0);
	let completedTopics = $state(0);
	let attemptsPerTrack = $state<{ track: string; count: number }[]>([]);

	let chart: Chart | null = null;

	async function loadAnalytics() {
		const res = await fetch('/api/analytics');
		if (!res.ok) {
			throw new Error('Failed to load analytics');
		}
		const data = await res.json();
		totalUsers = data.total_users;
		totalQuizAttempts = data.total_quiz_attempts;
		averageScore = data.average_score;
		completedTopics = data.completed_topics;
		attemptsPerTrack = data.attempts_per_track;

		if (browser) {
			if (chart) {
				chart.destroy();
			}
			const ctx = document.getElementById('trackAttemptsChart') as HTMLCanvasElement;
			chart = new Chart(ctx, {
				type: 'bar',
				data: {
					labels: attemptsPerTrack.map(item => item.track),
					datasets: [{
						label: 'Quiz Attempts per Track',
						data: attemptsPerTrack.map(item => item.count),
						backgroundColor: 'rgba(54, 162, 235, 0.5)',
						borderColor: 'rgba(54, 162, 235, 1)',
						borderWidth: 1
					}]
				},
				options: {
					scales: {
						y: {
							beginAtZero: true,
							ticks: {
								precision: 0
							}
						}
					}
				}
			});
		}
	}

	onMount(() => {
		loadAnalytics().catch(console.error);
	});
</script>

<div class="analytics-page">
	<h1>Analytics Dashboard</h1>

	<div class="metrics">
		<div class="metric-card">
			<h2>Total Users</h2>
			<p>{totalUsers}</p>
		</div>
		<div class="metric-card">
			<h2>Total Quiz Attempts</h2>
			<p>{totalQuizAttempts}</p>
		</div>
		<div class="metric-card">
			<h2>Average Score</h2>
			<p>{averageScore.toFixed(2)}%</p>
		</div>
		<div class="metric-card">
			<h2>Completed Topics</h2>
			<p>{completedTopics}</p>
		</div>
	</div>

	<div class="chart-container">
		<canvas id="trackAttemptsChart"></canvas>
	</div>
</div>

<style>
	.analytics-page {
		padding: 2rem;
		max-width: 1200px;
		margin: 0 auto;
	}

	h1 {
		text-align: center;
		margin-bottom: 2rem;
		color: #333;
	}

	.metrics {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 1.5rem;
		margin-bottom: 2rem;
	}

	.metric-card {
		background: white;
		border-radius: 8px;
		padding: 1.5rem;
		text-align: center;
		box-shadow: 0 2px 4px rgba(0,0,0,0.1);
	}

	.metric-card h2 {
		margin: 0 0 0.5rem 0;
		color: #666;
		font-size: 1rem;
	}

	.metric-card p {
		margin: 0;
		font-size: 2rem;
		font-weight: bold;
		color: #333;
	}

	.chart-container {
		background: white;
		border-radius: 8px;
		padding: 1.5rem;
		box-shadow: 0 2px 4px rgba(0,0,0,0.1);
	}

	canvas {
		max-width: 100%;
		height: 400px;
	}
</style>