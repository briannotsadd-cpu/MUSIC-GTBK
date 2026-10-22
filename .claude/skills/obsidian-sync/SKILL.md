---
name: obsidian-sync
description: Record durable Nova knowledge (decisions, architecture, bugs with root cause, research, performance milestones, lessons, dev log) in the owner's Obsidian vault, and keep it consistent with the code. Use after major tasks, at session end, after checkpoints/milestones, or when asked to update Obsidian.
argument-hint: "[task | checkpoint | milestone | session-end]"
---

# Obsidian sync: $ARGUMENTS (default: task)

Obsidian is the **human-readable knowledge base**. The repository (code, tests, `PROJECT_STATE.md`, `DECISIONS.md`) is the source of truth.
If a note and the implementation disagree, the implementation and its tests win. Fix the note.
Never paste chat transcripts, logs, long source code or decompiled output into the vault.

## Step 0: locate the vault (never guess)
1. Vault path = env `NOVA_VAULT_PATH`, else `.claude/settings.local.json` → `env.NOVA_VAULT_PATH` (per-machine, gitignored).
2. Valid only if `<path>/.obsidian/` exists. Otherwise **stop and ask the owner**. Do not search the disk for substitutes and do not create a vault.
3. If the vault is unreachable (e.g. a cloud session), write nothing there. Put the draft note in the reply. If the owner agrees, save it to `OBSIDIAN_PENDING.md` in the repo root (gitignored; `.claude/` is write-protected),
   and say that it is pending for the owner or a local session to apply.
4. Use the existing folder layout and naming. Create a folder only when its first real note exists.

## Step 1: should this be a note? (all notes must help UNDERSTAND, DECIDE, BUILD, DEBUG, LEARN or PLAN)
Write only if the information is likely to be reused, affects architecture, is a decision, or will help a future debug.
Trigger events: major feature, architecture change, critical bug found or fixed, new tech debt, finished research,
performance change, release, product decision, new AI capability, major limitation. Otherwise skip.

## Step 2: update before you create
- Search the vault for the concept (`grep -ril "<term>" "$NOVA_VAULT_PATH"`, plus file names and aliases). One concept = one note name. No `Sandbox`/`Sandboxing`/`Plugin Sandbox` triplets.
- Existing note: edit it in place and preserve everything the owner wrote. Never delete or rewrite their text. Reorganizing means moving to `99 - Archive`, not deleting. If unsure, don't touch it.
- Otherwise create it from `templates.md` with the right type.

## Step 3: write
- Explain WHY, architecture, behavior and knowledge. Reference code by path (`src/plugin-host/`), never copy it (max ~10 lines for a key snippet).
- Statuses: IDEA, RESEARCH, PLANNED, IN-PROGRESS, IMPLEMENTED, VERIFIED, BLOCKED, DEPRECATED. **VERIFIED only with test/benchmark evidence** (cite the command and exit code). Never "DONE".
- Frontmatter: only `project, type, status, priority, updated, tags`. Tags only from: nova, audio-engine, dsp, plugin, ai, architecture, bug, research, decision, performance, testing, p0, p1, p2.
- Links `[[Exact Note Name]]` only for real relationships (dependency, architecture, research, bug, decision, feature). No decorative links. Every new note links to at least one existing note, and is linked from one (its hub, the Dashboard or the Project Map).
- Development log entries are short (Completed / Fixed / Found / Next / Notes). If several log entries repeat a topic, distill it into the architecture/knowledge note (the log is history, the architecture note is current knowledge).

## Step 4: by mode
- **task:** a note for what changed (What Changed, Why, Implementation, Files Changed, Architecture Impact, Testing, Result, Problems Found, Remaining Work, Related), plus a dev-log line. Fixed bugs get a Bug note with a *root cause*, a verification and a regression test.
- **session-end:** `PROJECT_STATE.md` and repo docs first, then the relevant notes, the dev log, and the Dashboard if priority/status changed. Then check for duplicates, broken `[[links]]` and notes that contradict the code.
- **checkpoint:** also refresh Dashboard (status, P0/P1/P2, problems, next actions), architecture changes, tech debt, roadmap, research findings.
- **milestone:** create `MILESTONE - <name>` (What We Built, What Works, What Doesn't, Architecture Changes, Performance, Important Bugs, Lessons, Tech Debt, Next Milestone) linked from the Dashboard and the roadmap.

## Reading (long-term memory)
At task start, read only the notes for the current subsystem (found via the Project Map and a keyword search). Never load the whole vault.
Verify a note against the code before relying on it.

## Definition of Done
- The vault path was verified (or the pending-file fallback was used and reported).
- Every claim in the new or updated notes matches the code or test evidence from this session.
- No existing owner content was removed. No duplicate note exists. All new links resolve.
- Report: notes created, notes updated, and any note found stale against the code.
