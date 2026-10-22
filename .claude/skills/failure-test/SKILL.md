---
name: failure-test
description: Fault-injection testing for the plugin host (crash, hang, NaN, bad state, scan failure) and offline render (cancel, plugin failure, disk full, offline-vs-realtime null test). Use after plugin-host or render changes and before releases.
argument-hint: "plugin|render"
---

# Failure test: $ARGUMENTS

Requires the test-plugin fixture (a deliberately misbehaving plugin built in the test tree) and the render test harness.
If either is missing, report `NOT TESTABLE: <missing fixture>`, add creating it to `NEXT_ACTIONS.md`, and stop. Never simulate results.

## plugin: inject each fault and record the outcome
| Fault | Expected |
|---|---|
| segfault in process() | host process dies; DAW keeps running; track bypassed; user notified; restart restores state |
| infinite loop in process() | watchdog trips within N blocks; silence/bypass; process killed and restarted |
| hang in UI/editor open | DAW UI stays responsive |
| NaN/Inf output | output muted/sanitized; plugin flagged |
| corrupt/oversized state chunk on load | rejected with error; no crash, no unbounded allocation |
| crash during scan | plugin quarantined; scan continues; next startup skips it |
| latency change at runtime | delay compensation updates |
| malformed IPC message | rejected; connection reset; no DAW crash |

## render: run each scenario and record the outcome
| Scenario | Expected |
|---|---|
| cancel at 50% | job canceled quickly; no output file left |
| plugin crash mid-render | documented policy applied; job ends; never hangs |
| disk full / write error | job fails with a clear error; no file presented as complete |
| offline vs realtime | null test within the documented tolerance |
| UI thread during render | stays responsive (no render work on main thread) |

## Output
One row per case: `PASS / FAIL / NOT TESTABLE` + evidence (test name, command → exit, log excerpt).

## Definition of Done
- Every row was executed in this session or marked NOT TESTABLE with the reason.
- Each FAIL becomes a `NEXT_ACTIONS.md` item (P0 if it can crash the DAW or lose user data).
