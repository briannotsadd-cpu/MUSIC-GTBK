# Nova DAW (repo: MUSIC-GTBK)

Digital audio workstation. **Status: PRE-CODE.** No source, build system or tests exist yet.
Do not describe any subsystem as working; there is nothing to run. See `PROJECT_STATE.md`.

**Feature freeze (owner instruction, 2026-10-22):** do not add Nova features until the owner lifts it.
Allowed work: project infrastructure, decisions, docs, tooling.

## Start of every session
1. Read `PROJECT_STATE.md` (short) and the top of `NEXT_ACTIONS.md`.
2. `git status`, `git log --oneline -10`, `git diff --stat`. Never overwrite uncommitted changes you did not make.
3. After context compaction or a lost thread, run `/context-recovery`. Do not restart work from memory.

## Source of truth
| Topic | File |
|---|---|
| Current state, P0/P1/P2, last verification | `PROJECT_STATE.md` |
| Ordered task queue | `NEXT_ACTIONS.md` |
| Architecture (target and actual) | `ARCHITECTURE.md` |
| Decisions and their reasons (append-only) | `DECISIONS.md` |
| Subsystem rules (load automatically by path) | `.claude/rules/*.md` |
| Verification commands | `scripts/verify.sh` |

| Human knowledge base (why, lessons, research, history) | Owner's Obsidian vault (`$NOVA_VAULT_PATH`), via `/obsidian-sync`. Never overrides code or tests |

Create `KNOWN_ISSUES.md` and `TECH_DEBT.md` when their first real entry exists. Do not create empty trackers.
Facts live in one file only; elsewhere, link to them.

## Stack and layout
Not chosen yet (P0 in `NEXT_ACTIONS.md`). Record the choice in `DECISIONS.md`, then update this section with:
language and standard, framework, plugin formats, target platforms, the directory map, and build and test commands.

## Build and verify
- `scripts/verify.sh fast`: format check, compile, unit tests. Run after each small change.
- `scripts/verify.sh full`: adds the sanitizer build, every test label and stress tests. Run before calling a major feature complete.
- Exit codes: `0` checks ran and passed; `1` a check failed; `3` nothing could be verified (no build system yet).
  Exit `3` is **not** a pass.

## Non-negotiable constraints (details in `.claude/rules/`)
- **Audio thread:** never allocate, lock without a bound, do I/O, log expensively, block on IPC, run inference, scan plugins or encode files.
  Every realtime change states its deadline, allocation, locking, thread-ownership and dropout impact.
- **Third-party plugins are untrusted code.** Thread isolation is not crash isolation. Plugins run out of process, with a watchdog.
- **Offline render never runs on the main/UI thread.** It is cancelable, observable and survives plugin failure.
- **DSP changes are tested** across sample rates, channel layouts, silence, impulse, NaN/Inf, denormals, extreme parameters and automation.
  No unexplained magic constants.
- **No proprietary code copying.** Reverse engineering is for studying behavior only, where lawful.

## Definition of Done
A task is done only with evidence: test output, a runtime check, a benchmark or a diff review.
- Compiles only → `IMPLEMENTED — NOT VERIFIED`.
- `fast` passed → `VERIFIED (fast)`. Never claim "production ready" from `fast` alone.
- Major feature → `full` passed, plus an independent review (`/code-review`) and `/failure-test` where it applies.
Afterwards, update `PROJECT_STATE.md` (`/handoff`).

## Obsidian (second brain, not a chat archive)
After major work, a bug fix with root cause, a decision, finished research, or at session end, run `/obsidian-sync`.
The vault path comes from `NOVA_VAULT_PATH`; if it is unset or invalid, ask. Never guess a path or create a vault.
Never delete the owner's notes. Never paste transcripts or long code. If a note contradicts the code, the code wins; fix the note.

## Research before guessing
Unsure about VST3, CLAP, AU, JUCE, C++, OS audio APIs, threading or dependency versions? Read the docs or the source first
(`researcher` agent). Cite what you used. Never invent an API.

## Agents and skills
- Agents: `architect` (impact analysis, read-only), `audio-dsp`, `plugin-host`, `qa` (tries to break things), `researcher`.
  Reviews use built-in `/code-review`; security uses `/security-review`.
- Skills: `/context-recovery`, `/reality-check`, `/verify`, `/bug-hunt`, `/realtime-review`, `/failure-test`, `/handoff`.
- Critical features follow research → architect → implement → independent review → QA.
  Never let two agents edit the same file at the same time.
- Effort: routine `medium`; multi-file `high`; architecture, race, deadlock, realtime or plugin-isolation work `xhigh`.
  If work fails from incomplete reading or no tests, raise effort. If it reasons wrongly despite full effort, use a stronger model.

## Git
Check clean or dirty state before large work. No `reset --hard`, `clean -f`, force-push or branch deletion without explicit permission
(a hook enforces this). Re-read your own diff as a reviewer before committing.
