<script lang="ts">
	import { cn } from '$lib/theme';

	interface Props {
		code: string;
		language?: 'html' | 'javascript' | 'sql' | 'http';
		readonly?: boolean;
		title?: string;
		className?: string;
		onchange?: (code: string) => void;
	}

	let { code = $bindable(), language = 'html', readonly = false, title, className = '', onchange }: Props = $props();

	// Simple syntax highlighting
	function highlight(text: string, lang: string): string {
		let result = text
			.replace(/&/g, '&amp;')
			.replace(/</g, '&lt;')
			.replace(/>/g, '&gt;');
		
		if (lang === 'html') {
			// HTML tags
			result = result.replace(/(&lt;\/?)([\w-]+)/g, '$1<span class="text-brand">$2</span>');
			// Attributes
			result = result.replace(/(\s)([\w-]+)(=)/g, '$1<span class="text-warning">$2</span>$3');
			// Strings
			result = result.replace(/"([^"]*)"/g, '<span class="text-success">"$1"</span>');
			result = result.replace(/'([^']*)'/g, "<span class=\"text-success\">'$1'</span>");
		} else if (lang === 'javascript') {
			// Keywords
			const keywords = ['const', 'let', 'var', 'function', 'return', 'if', 'else', 'for', 'while', 'document', 'window', 'alert', 'fetch', 'async', 'await'];
			keywords.forEach(kw => {
				result = result.replace(new RegExp(`\\b(${kw})\\b`, 'g'), '<span class="text-brand">$1</span>');
			});
			// Strings
			result = result.replace(/"([^"]*)"/g, '<span class="text-success">"$1"</span>');
			result = result.replace(/'([^']*)'/g, "<span class=\"text-success\">'$1'</span>");
			result = result.replace(/`([^`]*)`/g, '<span class="text-success">`$1`</span>');
			// Comments
			result = result.replace(/(\/\/.*)/g, '<span class="text-text-muted">$1</span>');
		} else if (lang === 'sql') {
			// SQL keywords
			const keywords = ['SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'TABLE', 'AND', 'OR', 'INTO', 'VALUES', 'SET', 'JOIN', 'ON', 'ORDER', 'BY', 'LIMIT', 'UNION', '--'];
			keywords.forEach(kw => {
				result = result.replace(new RegExp(`\\b(${kw})\\b`, 'gi'), '<span class="text-brand">$1</span>');
			});
			// Strings
			result = result.replace(/'([^']*)'/g, "<span class=\"text-success\">'$1'</span>");
			// Comments
			result = result.replace(/(--.*)/g, '<span class="text-text-muted">$1</span>');
		} else if (lang === 'http') {
			// HTTP methods
			result = result.replace(/^(GET|POST|PUT|DELETE|PATCH)/gm, '<span class="text-brand">$1</span>');
			// Headers
			result = result.replace(/^([\w-]+):/gm, '<span class="text-warning">$1</span>:');
		}
		
		return result;
	}

	function handleInput(e: Event) {
		const target = e.target as HTMLTextAreaElement;
		code = target.value;
		onchange?.(code);
	}

	const lines = $derived(code.split('\n'));
</script>

<div class={cn("rounded-lg border border-border bg-canvas overflow-hidden", className)}>
	{#if title}
		<div class="flex items-center gap-2 border-b border-border bg-muted px-4 py-2">
			<div class="flex gap-1.5">
				<span class="size-3 rounded-full bg-danger/60"></span>
				<span class="size-3 rounded-full bg-warning/60"></span>
				<span class="size-3 rounded-full bg-success/60"></span>
			</div>
			<span class="text-xs font-medium text-text-muted">{title}</span>
		</div>
	{/if}
	
	<div class="relative font-mono text-sm">
		<!-- Line numbers -->
		<div class="absolute left-0 top-0 bottom-0 w-10 border-r border-border bg-muted/50 select-none" aria-hidden="true">
			<div class="py-3 px-2 text-right">
				{#each lines as _, i}
					<div class="leading-6 text-xs text-text-muted">{i + 1}</div>
				{/each}
			</div>
		</div>
		
		{#if readonly}
			<div class="pl-12 pr-4 py-3 overflow-x-auto min-h-[120px]">
				<pre class="leading-6 text-text whitespace-pre-wrap">{@html highlight(code, language)}</pre>
			</div>
		{:else}
			<div class="relative pl-12 pr-4 py-3 min-h-[150px]">
				<!-- Highlighted overlay -->
				<pre class="absolute inset-0 pl-12 pr-4 py-3 leading-6 text-text whitespace-pre-wrap pointer-events-none overflow-hidden" aria-hidden="true">{@html highlight(code, language)}</pre>
				
				<!-- Editable textarea -->
				<textarea
					class="w-full h-full min-h-[120px] bg-transparent leading-6 text-transparent caret-text resize-y outline-none"
					value={code}
					oninput={handleInput}
					rows={Math.max(lines.length, 5)}
					spellcheck="false"
					autocomplete="off"
					autocorrect="off"
					autocapitalize="off"
				></textarea>
			</div>
		{/if}
	</div>
</div>
