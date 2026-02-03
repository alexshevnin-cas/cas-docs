# CAS Platform Documentation

Purpose:
This repository contains high-level documentation of the CAS platform.
The goal is to provide a shared source of truth for humans and AI agents.

How to read:
1. Start with /01-platform/platform-overview.md
2. Then read /02-business-model/cas-business-model.md
3. Then read /03-user-cabinet/user-cabinet-overview.md
4. Then read /04-bi/bi-overview.md

Scope:
- High-level platform structure
- Business model
- User-facing cabinet
- BI and metrics

Out of scope (for now):
- SDK technical details
- Payments mechanics
- Publishing internals

Update rules:
- Prefer clarity over completeness
- Do not add details without explicit need
- Each document should stay at a single abstraction level

# CAS Platform Documentation

## What this repo is
A lightweight, top-down documentation repo for the CAS platform.
It is designed to be:
- readable for humans
- easy to evolve over time
- usable as structured context for AI agents (Claude Code / ChatGPT)

## How we will work (human workflow)
We’ll improve one document at a time.
For each file:
1. Clarify purpose and boundaries (what is in scope / out of scope)
2. Add only high-level facts we are sure about
3. Keep a consistent structure
4. Commit changes to Git

## How Claude Code should use this repo
Claude Code should NOT try to load everything.
Instead:
1. Always start with this README
2. Load only the documents needed for the current task
3. If details are missing, ask questions and propose where to add a new section/file
4. Never invent missing product facts

## Reading order
1. `/01-platform/platform-overview.md`
2. `/02-business-model/cas-business-model.md`
3. `/03-user-cabinet/user-cabinet-overview.md`
4. `/04-bi/bi-overview.md`
5. `/90-ai/ai-context-rules.md`

## Scope (for now)
- High-level platform structure
- Business model
- User-facing cabinet
- BI and metrics

## Out of scope (for now)
- SDK technical details
- Payments mechanics
- Publishing internals

## Document conventions
- Keep one abstraction level per document (no mixing deep tech + business + UI)
- Prefer clarity over completeness
- Use short sections and bullet points
- Add links to other docs when needed

## Repo structure
- `01-platform/` — what CAS is, top-level components
- `02-business-model/` — value, revenue streams, constraints
- `03-user-cabinet/` — user-facing cabinet goals and blocks
- `04-bi/` — BI overview and metrics dictionary
- `90-ai/` — rules for AI agents using this repo

## Change log
- v0: initial skeleton