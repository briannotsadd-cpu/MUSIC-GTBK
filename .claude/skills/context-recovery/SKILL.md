---
name: context-recovery
description: Rebuild the current task from project files and git after context compaction, a new session, or when unsure what was in progress. Use before continuing any interrupted work.
---

# Context recovery

Goal: reconstruct the current task from durable evidence, not conversation memory. Never restart a system you can't remember. Find it first.

## Procedure
1. **Instructions:** CLAUDE.md is already loaded; re-read its "Non-negotiable constraints" and "Definition of Done".
2. **State:** read `PROJECT_STATE.md` and the top 5 items of `NEXT_ACTIONS.md`.
3. **Git:**
   - `git status --short`, `git branch --show-current`, `git log --oneline -15`
   - `git diff --stat` and `git diff --stat --cached`, then read the full diff of the files involved.
   - `git stash list` (unfinished work may be stashed).
4. **Last verification:** `cat .claude/state/last-verify` (format: mode result hash time), and compare with `scripts/verify.sh --state-hash`.
5. **Affected subsystem:** from the changed paths, read the matching `.claude/rules/*.md`, the relevant `ARCHITECTURE.md` section,
   and the actual implementation files (not just the diff hunks).
   Search for existing implementations before assuming something is missing.
6. **Tests:** run `scripts/verify.sh fast` (or the narrowest relevant test target). Record the exit code.
7. **Reconstruct:** write the recovery summary below. If the task is still ambiguous, ask the user rather than guessing.

## Output
```
RECOVERED TASK: <one line>
EVIDENCE: <commits / diff files / NEXT_ACTIONS item that show it>
DONE SO FAR: <bullets, each with evidence>
REMAINING: <bullets>
VERIFY: <command> → exit <n> (<pass/fail/3 = nothing verifiable>)
RISKS: <uncommitted work not mine, failing tests, unclear intent>
```

## Definition of Done
- Every claim in the summary cites a file, commit, diff or command output.
- The test command was actually run this session.
- No code was changed during recovery.
