---
name: reality-check
description: Audit what actually works vs what is claimed. Classify each subsystem COMPLETE/PARTIAL/BROKEN/MOCK/NOT STARTED with evidence and update PROJECT_STATE.md. Use for project audits, before planning, or when status claims look doubtful.
argument-hint: "[subsystem or path, default: all]"
---

# Reality check: $ARGUMENTS

## Procedure
1. **Scope:** use the subsystem or path given (default: every row in `PROJECT_STATE.md` § Systems, plus any top-level source directory not listed).
2. **Inspect the implementation:** for each subsystem, find its entry points and read them (definitions, not just names).
3. **Verify the runtime path:** trace from a real entry point (app start, audio callback, UI action, CLI or test) to the code.
   Code not reachable from any entry point is at most PARTIAL.
4. **Find fakes:** search the scope for `TODO|FIXME|XXX|HACK|stub|mock|fake|dummy|placeholder|not implemented|unimplemented|return 0; *//|NotImplemented`,
   hard-coded returns, disabled tests (`DISABLED_`, `skip`, `#if 0`) and commented-out calls.
5. **Run tests:** `scripts/verify.sh fast` plus any label-specific `ctest -L <label>`. Record the commands and exit codes.
6. **Classify:**
   - COMPLETE: reachable, real implementation, covered by passing tests that would fail if it broke.
   - PARTIAL: real but missing cases, untested, or unreachable.
   - BROKEN: tests fail, crash, or contradicts its documentation.
   - MOCK: returns canned or fake data on the real path.
   - NOT STARTED: no implementation.
7. **Report** (table below), then update `PROJECT_STATE.md` § Systems and § Last verification in place.
8. **Fix** the single highest-priority BROKEN item only if the user asked for fixes. Otherwise list it at the top of `NEXT_ACTIONS.md`.

## Output
| Subsystem | Status | Evidence (file:line, test, command → exit) | Gap |
|---|---|---|---|

## Definition of Done
- Every row has evidence; "looks fine" is not evidence.
- The test commands were run in this session and their exit codes are shown.
- PROJECT_STATE.md is updated with no status upgraded beyond what the evidence supports.
