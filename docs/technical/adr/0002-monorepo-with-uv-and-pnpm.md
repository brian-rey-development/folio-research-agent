# 0002 Monorepo with uv and pnpm

This record has the status accepted, and the learner and Claude accepted it on 2026-11-03 during the Folio design.

## Context

Folio has a Python backend for the AI work and a Next.js web app. The Python side has five packages with a strict layer order, and the web app needs types that match the API.

## Decision

One repository holds everything. A uv workspace manages the Python packages and the API app with one lock file, and pnpm manages the single web app. A `justfile` gives one command for setup, checks and formatting across both toolchains. The Python checks use ruff for lint and format, ty for types, pytest for tests and import-linter for the layer order. The web checks use Oxlint for lint, with its type-aware mode, and TypeScript 7 for type checks.

## Alternatives

Separate repositories for the API and the web app give independent releases, but every API change then needs two pull requests. A Python-only stack gives one toolchain, but the UI quality and the brand suffer. Turborepo or Nx add value with many TypeScript packages, and Folio has only one. ESLint with typescript-eslint has more plugins than Oxlint, but typescript-eslint does not run on TypeScript 7. Three React plugins also do not accept ESLint 10 yet.

## Consequences

A change to an API schema and the matching web type lands in one commit. The cost is two package managers, which the `justfile` hides behind one set of commands. Oxlint and the Go-native TypeScript 7 compiler keep the web checks to a few seconds. A rule that exists only as an ESLint plugin needs a custom check.
