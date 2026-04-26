export function cn(...classes: Array<string | false | null | undefined>): string {
return classes.filter(Boolean).join(' ');
}

export const uiTokens = {
	pageWidth: 'mx-auto w-full max-w-6xl px-4 sm:px-6 lg:px-8',
	card: 'rounded-xl border border-border bg-surface text-text shadow-sm transition-all duration-200',
	cardMuted: 'rounded-xl border border-border bg-muted text-text shadow-sm transition-all duration-200',
	cardHover: 'rounded-xl border border-border bg-surface text-text shadow-sm transition-all duration-200 hover:border-brand-border hover:shadow-md hover:-translate-y-0.5',
	focusRing: 'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-2 focus-visible:ring-offset-canvas'
} as const;

export const buttonVariants = {
primary: 'bg-brand text-white hover:bg-brand-strong disabled:bg-border disabled:text-text-muted',
secondary: 'bg-surface text-text border border-border hover:bg-muted disabled:text-text-muted',
ghost: 'bg-transparent text-text hover:bg-muted disabled:text-text-muted',
danger: 'bg-danger text-white hover:bg-danger-strong disabled:bg-border disabled:text-text-muted'
} as const;

export const badgeVariants = {
neutral: 'bg-muted text-text border border-border',
success: 'bg-success-soft text-success border border-success-border',
warning: 'bg-warning-soft text-warning border border-warning-border',
danger: 'bg-danger-soft text-danger border border-danger-border',
brand: 'bg-brand-soft text-brand border border-brand-border'
} as const;

export const alertVariants = {
info: 'border-brand-border bg-brand-soft text-brand-strong',
success: 'border-success-border bg-success-soft text-success',
warning: 'border-warning-border bg-warning-soft text-warning',
danger: 'border-danger-border bg-danger-soft text-danger'
} as const;
