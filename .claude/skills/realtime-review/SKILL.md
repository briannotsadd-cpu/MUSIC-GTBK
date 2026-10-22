---
name: realtime-review
description: Review audio-thread, DSP or performance-sensitive changes for realtime safety (alloc, locks, IO, deadline), DSP correctness test coverage, and measured performance. Use for any diff touching the audio callback, DSP, or engine graph, and for performance investigations.
argument-hint: "[diff | path]"
---

# Realtime / DSP / performance review: $ARGUMENTS (default: diff)

## Procedure
1. **Collect:** `git diff HEAD` (or the path given). List the functions changed.
2. **Reachability:** for each changed function, determine whether it is reachable from the audio callback.
   Follow call chains, virtual dispatch and callbacks. Mark each RT, NON-RT or UNKNOWN; treat UNKNOWN as RT.
3. **Static audit of RT functions** against `.claude/rules/audio-realtime.md`:
   - allocation, including hidden ones: `std::function`, `std::string`, container growth, `shared_ptr` refcount drop to zero, exceptions
   - locks, syscalls, I/O, logging; unbounded loops over user-sized data
   - atomics: does the memory order justify the publication? Is there any false sharing on hot atomics?
4. **DSP checks** (if DSP changed): confirm tests exist for every item in `.claude/rules/dsp.md`. List the missing ones.
5. **Measure** (if a build exists):
   - run the relevant benchmark or stress test at the smallest buffer size and highest sample rate (bench labels `stress`/`bench`)
   - report worst case and p99 per-block time against the deadline (`buffer_size / sample_rate`)
   - compare with the base branch (`git stash` or a worktree) when claiming an improvement
6. **Verdict** per changed function.

## Output
| Function | RT? | Violations | DSP tests missing | Measured worst/p99 vs deadline |
|---|---|---|---|---|
Verdict: SAFE / UNSAFE (blocking issues listed) / UNVERIFIED (no build or benchmark).

## Definition of Done
- Every changed function is classified, and UNKNOWN reachability is treated as RT.
- Performance claims cite a measurement run in this session, with the before/after numbers.
- No "realtime safe" claim without either a measurement or an allocation/lock-detection test.
