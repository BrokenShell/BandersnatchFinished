# AGENTS

This guide captures the reusable engineering conventions for building Python-first web services with FastAPI, Jinja templates, and their supporting tools. It leans into a minimalist philosophy that keeps logic concentrated in the backend, keeps templates lean and declarative, and avoids extra moving parts unless they earn their keep. The goal is to move quickly while building codebases that are predictable, lightweight, and easy for new contributors to understand.

## Core Principles
- Build the app around Python first: route handlers, business rules, and integrations always live on the server side.
- Keep templates minimal and semantic; render complete pages from the backend rather than relying on client frameworks.
- Treat JavaScript as optional UI polish. Only add scripts for interactions that cannot be handled with HTML, CSS, or server responses. Prefer CDN embeds for occasional visualization helpers.
- Favor readability over verbosity. Let the code speak for itself, keep comments to a minimum, and only document non-obvious decisions.
- Handle errors with clear control flow. Use try/except blocks sparingly and never as substitutes for conditional logic.

## Tech Stack Baseline
- Python 3.x with FastAPI for async HTTP endpoints and dependency injection where needed.
- Jinja2 for server-side rendering with a shared base layout, block overrides, and small, focused templates.
- Static assets served from a predictable `/static` tree, leaning on plain CSS. Add JavaScript bundles only when absolutely necessary.
- Altair for chart definition with Vega/Vega-Lite embedding on the client when visualizations are required.
- MongoDB for persistence via `pymongo` and `motor`, promoted to DataFrame workflows with pandas when analytics or ML steps are involved.
- Scikit-learn for model training, persisted with `joblib` so trained models can be reused between requests.

## Project Layout & Patterns
- Keep the application package lightweight with focused modules rather than large monoliths.
- Initialize services (database connections, model instances, option lists, templates) at module import time so route handlers stay lean.
- Group imports at the top of every module, ordered by standard library, third-party, then local packages.
- Lean on type hints for public functions and methods when they clarify intent, but do not chase exhaustive annotations.
- Structure FastAPI endpoints as async callables returning `TemplateResponse` objects for HTML pages; prefer POST forms for mutating actions.

## HTML & Asset Conventions
- Keep HTML documents declarative. Extend a single base layout, override content blocks, and avoid inline styles or script tags unless essential.
- Prefer standard form controls and server round-trips for interactions. Use select elements and basic inputs to drive backend computations.
- Serve CSS resets and theme files from the static directory; avoid utility frameworks unless there is a compelling reason.
- When client-side visualizations are required, generate the JSON spec on the server and embed it with `vegaEmbed` or similar minimal shims.

## Dependency Management & Tooling
- Use `requirements.txt` with unpinned versions during development to keep velocity high.
- Once ready for production, pin packages with the `~= major.minor.patch` pattern (e.g., `package~=2.3.4`) to lock compatibility while still receiving security and patch updates.
- Provide `install.sh` for dependency setup (`pip install --upgrade pip setuptools wheel -r requirements.txt`). Keep it idempotent and shell-friendly.
- Provide `run.sh` for local execution (`uvicorn package.module:app`). Mirror the same command in a `Procfile` for deployment targets that expect it.

## Operational Habits
- Favor simple print-based diagnostics during development; introduce structured logging only when necessary.
- Cache or reuse heavy resources like database clients and trained models across requests to minimize latency.
- Keep the repository free of unnecessary scaffolding. Avoid over-engineering.
- When extending the project, add tests or scripts as appropriate, but keep them lightweight and aligned with the minimalist philosophy outlined above.
