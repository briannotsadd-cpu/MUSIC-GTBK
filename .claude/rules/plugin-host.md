---
paths:
  - "**/plugin*/**"
  - "**/host*/**"
  - "**/vst*/**"
  - "**/clap/**"
  - "**/au/**"
  - "**/sandbox/**"
  - "**/ipc/**"
---
# Plugin host rules
<!-- Globs are provisional until the directory layout is decided. -->

Third-party native plugins are **untrusted execution**. Thread isolation is not crash isolation: a segfault, abort or heap corruption in-process takes down the DAW.

Every plugin-host change must address:
- **Process isolation:** plugins load in a separate host process. The DAW process never `dlopen`s/`LoadLibrary`s third-party binaries.
- **IPC:** shared-memory audio buffers plus a control channel. Message schema is versioned. All plugin-provided sizes and strings are bounds-checked.
- **Crash handling:** host-process death is detected, the plugin is bypassed (audio continues), the user is notified, and the plugin is restarted with its last saved state.
- **Hang/watchdog:** a per-block deadline. On a miss, output silence or bypass for that block. Repeated misses lead to kill and restart.
  The audio thread never waits unbounded on IPC.
- **State restoration:** chunks are saved off the audio thread, validated on load, and versioned.
- **Scanning:** happens out of process, with a timeout per plugin. Crashers and hangers go to a **quarantine** list, so one bad plugin never blocks startup.
- **Output sanitizing:** NaN/Inf/denormal detection on plugin output, then mute and flag.
- **Latency:** read reported latency, re-query it on change, and feed delay compensation.

Use the API docs for VST3/CLAP/AU (`researcher` agent). Never guess SDK signatures. Test with `/failure-test plugin`.
