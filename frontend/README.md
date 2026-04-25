# CyberLearn Frontend

SvelteKit + Tailwind frontend scaffold for CyberLearn. The UI is intentionally neutral and token-driven so future Figma restyling can update visuals without changing feature logic.

## Stack

- Bun
- SvelteKit (Svelte 5)
- Tailwind CSS v4
- TypeScript + ESLint + Vitest

## Directory layout

- `src/lib/components`: reusable UI primitives
- `src/lib/layouts`: reusable page shell/layout wrappers
- `src/lib/stores`: state containers and session context
- `src/lib/services`: Flask API client layer
- `src/lib/theme`: design tokens and class helpers
- `src/routes`: page-level route containers

## Scripts

```bash
bun run dev
bun run check
bun run lint
bun run test
bun run build
```

## API contract targets

The service layer is wired for the following Flask endpoints:

- `GET /api/dashboard`
- `GET /api/tracks`
- `GET /api/tracks/:id/modules`
- `GET /api/quizzes/:id`
- `POST /api/quizzes/:id/submit`
- `GET /api/progress`
- `POST /api/progress`
- `POST /api/analyze-message`
- `GET /api/message-history`
