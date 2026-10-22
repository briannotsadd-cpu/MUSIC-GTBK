---
paths:
  - "**/ui/**"
  - "**/gui/**"
  - "**/editor/**"
  - "**/views/**"
  - "**/widgets/**"
---
# UI rules
<!-- Globs are provisional until the directory layout is decided. -->

- The UI never touches audio-thread state directly. It reads meters and positions through atomics or lock-free snapshots, and writes through the command queue.
- No blocking work on the UI thread: file I/O, scanning, rendering and analysis go to workers, with progress shown.
- UI refresh is decoupled from the audio callback rate (coalesced timers). Meter updates must not allocate per frame.
- Parameter edits from the UI are smoothed or ramped on the audio side, never applied as discontinuous jumps that click.
