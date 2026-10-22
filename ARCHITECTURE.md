# Architecture — Nova DAW

**Status: NOT DESIGNED.** No code exists. This file holds the invariants any design must satisfy and the open questions.
When a design is chosen, replace "Open questions" with the actual subsystem map, thread model and data flow.
Mark each part `TARGET` or `IMPLEMENTED` so the design is never mistaken for reality.

## Invariants (from DECISIONS.md)
- **Threads:** audio thread (hard realtime) · UI/main thread · worker pool (disk, encoding, analysis, scanning) · render thread(s).
  Each piece of mutable state has exactly one owning thread. Other threads reach it only through messages or immutable snapshots.
- **UI ↔ audio:** lock-free bounded queues or atomically swapped immutable snapshots, preallocated.
  Memory is reclaimed off the audio thread.
- **Plugins:** separate host process(es), shared-memory audio buffers plus a control channel, watchdog deadline per block,
  crash leads to bypass + state restore + user notice.
- **Render:** a job object with cancel token, progress, and an error channel. Writes to a temp file, then renames atomically on success.
- **Project state:** single source of truth (document model) on the main thread. The audio engine consumes compiled, immutable graphs.

## Open questions (P0, the owner decides)
1. Language and standard (e.g. C++20/23, Rust) and the minimum compiler versions.
2. Framework: JUCE, custom, other. Licensing implications.
3. Plugin formats: VST3, CLAP, AU (macOS only), LV2.
4. Platforms and audio APIs: CoreAudio, WASAPI/ASIO, ALSA/JACK/PipeWire.
5. Build system and test framework.
6. UI technology.
7. Project file format and versioning/migration strategy.
