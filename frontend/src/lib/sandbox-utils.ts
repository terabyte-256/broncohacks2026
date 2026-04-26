export function createSandboxHTML(html: string): string {
return [
'<!DOCTYPE html><html><head><meta charset="UTF-8"><style>',
'* { box-sizing: border-box; }',
'body { font-family: system-ui, -apple-system, sans-serif; padding: 16px; margin: 0; background: #0a0a0f; color: #e4e4e7; font-size: 14px; line-height: 1.5; }',
'input, button, textarea, select { font-family: inherit; font-size: inherit; padding: 8px 12px; border-radius: 6px; border: 1px solid #27272a; background: #18181b; color: #e4e4e7; }',
'input:focus, textarea:focus, select:focus { outline: none; border-color: #22d3ee; }',
'button { background: #22d3ee; color: #0a0a0f; border: none; cursor: pointer; font-weight: 500; }',
'button:hover { background: #06b6d4; }',
'form { display: flex; flex-direction: column; gap: 12px; }',
'label { display: flex; flex-direction: column; gap: 4px; font-size: 13px; color: #a1a1aa; }',
'.comment { color: #a1a1aa; margin: 8px 0; padding: 12px; background: #18181b; border-radius: 8px; border: 1px solid #27272a; }',
'h1, h2, h3 { color: #f4f4f5; margin: 0 0 12px 0; }',
'a { color: #22d3ee; }',
'img { max-width: 100%; }',
'</style></head><body>',
html,
'<script>',
'window.alert = function(msg) { window.parent.postMessage({ type: "sandbox-alert", message: String(msg) }, "*"); };',
'const originalLog = console.log;',
'console.log = function(...args) { window.parent.postMessage({ type: "sandbox-log", message: args.join(" ") }, "*"); originalLog.apply(console, args); };',
'window.onerror = function(msg) { return false; };',
'<\/script></body></html>'
].join('');
}
