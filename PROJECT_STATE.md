# Project State — Nova DAW

> Read this at session start. Keep it under ~80 lines. Overwrite sections in place; never append transcripts.
> Status words: COMPLETE / PARTIAL / BROKEN / MOCK / NOT STARTED, each backed by evidence.

**Last updated:** 2026-10-22 · **By:** Claude (project-intelligence setup)

## Current architecture
None implemented. Target constraints are recorded in `ARCHITECTURE.md` and `DECISIONS.md`.

## Systems
| System | Status | Evidence |
|---|---|---|
| Audio engine | NOT STARTED | no source in repo |
| DSP | NOT STARTED | — |
| Plugin host | NOT STARTED | — |
| Offline render | NOT STARTED | — |
| Project file / state | NOT STARTED | — |
| UI | NOT STARTED | — |
| Build system / tests | NOT STARTED | `scripts/verify.sh` exits 3 |
| Claude project-intelligence setup | IMPLEMENTED | this commit; hooks smoke-tested with sample input |

Working: none. Partial: none. Known broken: none (nothing exists yet).

## Priorities
- **P0:** choose the stack (language, framework, plugin formats, platforms) and the directory layout. Everything else waits on this.
- **P1:** build-system skeleton plus a test harness so `scripts/verify.sh fast` exits 0.
- **P2:** realtime engine skeleton (audio callback, lock-free UI↔audio messaging) with allocation and lock tests.

## Constraints in force
- Feature freeze on Nova features (owner, 2026-10-22).
- Realtime, plugin-isolation, render and DSP rules: `CLAUDE.md` § Non-negotiable constraints.

## Blockers
- The Obsidian vault location is unknown (not reachable from the cloud session).
- The owner must decide P0 (stack and platforms). Agents must not choose it unilaterally.

## Recent major changes
- 2026-10-23: added `/obsidian-sync` + D-007 (Obsidian knowledge base). Vault NOT located; no notes written. IMPLEMENTED — NOT VERIFIED against a real vault.
- 2026-10-22: added the Claude Code project-intelligence system (CLAUDE.md, rules, skills, agents, hooks, verify script).

## Last verification
- 2026-10-22 · `scripts/verify.sh fast` → exit 3 (no build system in this repo).
- 2026-10-22 · Tooling: verify.sh fast/full run against a scratch CMake project (pass → 0; formatting error → 1; ASan caught a heap overflow → 1).
  Hooks were tested with sample JSON: 19 guard cases, the Stop gate, realtime flags and both SessionStart modes.
  A fresh headless session answered all onboarding questions from the repo files.
