---
name: handoff
description: Save durable project state at the end of a significant task so a fresh session (or post-compaction context) can continue. Updates PROJECT_STATE.md, NEXT_ACTIONS.md, and DECISIONS.md from evidence. Use after finishing or pausing major work.
---

# Handoff

## Procedure
1. `git status --short`, `git diff --stat`, `git log --oneline -10`: what changed in this task.
2. Run `scripts/verify.sh fast` if source changed and the stamp is stale (`.claude/state/last-verify`). Record the exit code.
3. Re-read your own diff as an independent reviewer: look for leftover debug code, TODOs you added, unrelated edits, and secrets.
4. Update `PROJECT_STATE.md` **in place**. Keep it under ~80 lines:
   - Systems table: change status only with evidence.
   - Priorities, blockers, recent major changes (one line each; drop entries older than ~5).
   - Last verification: date, command, exit code.
5. Update `NEXT_ACTIONS.md`: remove finished items, and add discovered work in priority order. The top item = what the next session should start on.
6. Append to `DECISIONS.md` for any architectural choice made (D-NNN format). Never rewrite old entries.
7. Create or append `KNOWN_ISSUES.md` / `TECH_DEBT.md` only for real new entries.
8. Run `/obsidian-sync session-end` (notes, dev log, Dashboard). If the vault is unreachable, report the notes as pending.
9. Commit the docs with the code when the user has asked for commits; otherwise leave them staged-ready and say so.

## Definition of Done
- A new session reading only CLAUDE.md, PROJECT_STATE.md, NEXT_ACTIONS.md and git could continue without this conversation.
- No transcript, logs or speculation was written into the state files.
- Obsidian is updated, or reported as pending with the reason.
- Every status matches the evidence (unverified work says `IMPLEMENTED — NOT VERIFIED`).
