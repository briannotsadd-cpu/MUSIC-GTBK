---
name: bug-hunt
description: Systematically find real bugs in a subsystem or diff (races, lifetime, realtime violations, numeric edge cases, error paths), prove each with a failing test or reproduction, and rank them. Use when asked to find bugs, harden code, or investigate flaky behavior.
argument-hint: "[path, subsystem, or 'diff']"
---

# Bug hunt: $ARGUMENTS

## Procedure
1. **Scope:** for `diff`, use `git diff HEAD` plus the callers of the changed functions. Otherwise use the given path or subsystem.
2. **Map threads:** for each mutable object in scope, note the owning thread and every thread that touches it.
   Any object touched by more than one thread without atomics or a message handoff is a candidate race.
3. **Check each category, in order:**
   - data races / memory ordering (relaxed atomics publishing non-atomic data, ABA in lock-free queues)
   - lifetime: use-after-free across threads, dangling references into containers, plugin unload while in use
   - realtime violations (the `.claude/rules/audio-realtime.md` list)
   - numeric: NaN/Inf, denormals, division by zero, integer overflow in sample counts (>2^31 at 192k after ~3 h), float→int conversions
   - error paths: ignored return codes, exceptions crossing C ABI or thread boundaries, partial writes
   - input validation: project files, plugin state chunks, IPC messages
   - shutdown and order of destruction; device change mid-stream; sample-rate or buffer-size change
4. **Prove it:** each candidate needs a failing test, a sanitizer report (`scripts/verify.sh full`), or a concrete reproduction.
   Unproven candidates go in a separate "suspected" list.
5. **Rank** by severity: crash or data loss > audible glitch > wrong output > cosmetic. Then by likelihood.

## Output
| # | Severity | Location | Bug | Proof (test / sanitizer / repro) | Suggested fix |
|---|---|---|---|---|---|
Plus a "Suspected (unproven)" list.

## Definition of Done
- Every confirmed bug has proof that was run in this session.
- No fixes are applied unless requested. If they are, each fix comes with its regression test.
