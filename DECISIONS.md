# Decisions (append-only)

> Format: `D-NNN · date · status (ACCEPTED/SUPERSEDED by D-xxx) · decision · reason · consequences`.
> Never edit an accepted decision's text; supersede it with a new entry.

**D-001 · 2026-10-22 · ACCEPTED · Audio thread is hard-realtime.**
No allocation, unbounded locks, I/O (disk, network, database), blocking IPC, expensive logging, AI inference, plugin scanning or file encoding in the audio callback.
Reason: any of these can miss the buffer deadline and cause audible dropouts. Consequence: cross-thread data goes through preallocated lock-free structures.

**D-002 · 2026-10-22 · ACCEPTED · Third-party plugins are untrusted execution.**
Host them out of process, with IPC, a watchdog for hangs, crash recovery with state restore, quarantine for repeat offenders, and NaN/Inf sanitizing of their output.
Reason: a thread cannot contain a crash or memory corruption in native code. Consequence: plugin latency and IPC cost must be measured and compensated.

**D-003 · 2026-10-22 · ACCEPTED · Offline render runs off the main/UI thread.**
It is cancelable, reports progress, survives plugin failure, and never writes a partial file as if complete.

**D-004 · 2026-10-22 · ACCEPTED · Evidence-based status.**
Claims of DONE/FIXED/PRODUCTION READY require test, runtime, benchmark or crash-test evidence. Otherwise use `IMPLEMENTED — NOT VERIFIED`.

**D-005 · 2026-10-22 · ACCEPTED · Clean-room research.**
Reverse engineering is used only to study behavior and architecture, where lawful. No proprietary code is copied.

**D-006 · 2026-10-22 · ACCEPTED · Feature freeze.**
No Nova features until the owner lifts it. Project infrastructure only.
