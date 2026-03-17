# AGENTS.md — Frontend (Lab Notebook AI Assistant)

## Scope
This file governs work inside `apps/web`.

## Product Context
This frontend is the UI for **Lab Notebook AI Assistant**, an AI-powered lab notebook for managing experiments, viewing experiment history, and interacting with an AI assistant connected to backend tools and Azure Foundry agents.

## Tech Stack
- Next.js App Router
- TypeScript
- Tailwind CSS v4
- React 19
- ESLint

## Primary Goals
- Build a clean, modern, professional UI for a lab notebook product.
- Keep the codebase maintainable, typed, and easy to refactor.
- Separate UI concerns from data fetching and business logic.
- Make it easy to connect later with backend APIs and Azure agent features.

## Design Direction
- Visual style inspired by: Notion, Linear, Vercel dashboard
- Clean, minimal, spacious UI
- Light theme first
- Strong hierarchy, subtle borders, soft shadows
- Avoid noisy gradients and overdesigned dashboards
- Prioritize readability and fast navigation

## App Structure
Use this structure unless there is a strong reason not to:

src/
  app/
  components/
    ui/
    layout/
    dashboard/
    experiments/
    chat/
  lib/
    api/
    utils/
    constants/
  hooks/
  types/

### Folder rules
- `app/`: routes, layouts, page-level composition
- `components/ui/`: generic reusable UI primitives
- `components/layout/`: shell layout components (sidebar, topbar, containers)
- `components/dashboard/`: dashboard-specific widgets/cards
- `components/experiments/`: experiment list/detail related UI
- `components/chat/`: AI assistant UI
- `lib/api/`: fetchers and API client helpers
- `lib/utils/`: pure utility functions only
- `types/`: shared frontend types

## Routing Conventions
Use App Router route groups where useful, but keep it simple.

Suggested routes:
- `/` → dashboard
- `/experiments` → experiment list
- `/experiments/[id]` → experiment detail
- `/assistant` → AI assistant view
- `/settings` → settings

## UI Rules
- Prefer server components by default.
- Use client components only when needed for interactivity.
- Keep components small and composable.
- Avoid giant page files with mixed concerns.
- Extract repeated UI patterns early.
- Use semantic HTML.
- Ensure responsive behavior from the start.

## Styling Rules
- Use Tailwind utilities directly in components.
- Avoid premature abstraction of tiny style patterns.
- Do not introduce custom CSS files unless truly necessary.
- Keep spacing consistent.
- Prefer subtle color usage.
- Use status badges for experiment states:
  - active
  - completed
  - failed
  - draft

## State Management
- Prefer local state for local UI concerns.
- Prefer URL/search params for filter state when useful.
- Do not introduce heavy state libraries unless clearly necessary.
- If async data is needed, isolate data access in `lib/api`.

## Data and API Integration
- Do not hardcode backend URLs in components.
- Centralize API access in `src/lib/api`.
- Use typed response models.
- Mock data is acceptable early, but keep mocks isolated and easy to replace.

## Accessibility
- Buttons must be real buttons.
- Inputs must have labels or accessible names.
- Ensure keyboard navigability for sidebar, dialogs, dropdowns, and chat input.
- Maintain sufficient contrast.

## Performance
- Avoid unnecessary client-side rendering.
- Avoid overusing `useEffect`.
- Avoid fetching in deeply nested UI components.
- Prefer top-level data loading patterns.

## Non-goals / Hard Rules
- Do not add Redux/Zustand unless explicitly justified.
- Do not add a component library unless requested.
- Do not overengineer design tokens.
- Do not mix backend business rules into frontend components.
- Do not introduce large dependencies for trivial problems.

## Coding Style
- Use TypeScript strictly.
- Prefer explicit prop types.
- Prefer named exports for reusable components.
- Keep files focused.
- Prefer readable code over clever code.

## Naming Conventions
- Components: PascalCase
- Hooks: `useX`
- Utilities: camelCase
- Route segment folders: lowercase
- Avoid vague names like `Card2`, `Helper`, `DataThing`

## Expected Key UI Areas
Build toward these product areas:
1. Dashboard
2. Experiments list
3. Experiment detail
4. AI assistant chat
5. Create new experiment flow

## Preferred Workflow for Changes
When implementing features:
1. Start with UI structure
2. Extract reusable components
3. Add typed mock data if backend is not ready
4. Integrate API through `lib/api`
5. Refine loading, empty, and error states

## Output Expectations for AI Coding Agents
When making changes:
- Preserve folder structure
- Keep changes small and reviewable
- Prefer production-ready code over placeholders
- Include loading and empty states when relevant
- Avoid unnecessary refactors outside the requested scope