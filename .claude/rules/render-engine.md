---
paths:
  - "**/render*/**"
  - "**/bounce*/**"
  - "**/export*/**"
---
# Offline render rules
<!-- Globs are provisional until the directory layout is decided. -->

- Never render on the main/UI thread. Render runs as a job on dedicated worker thread(s).
- **Cancelable:** a cancel token checked at least once per block. Cancel leaves no partial output file behind.
- **Observable:** progress (samples done / total), state (queued/running/canceled/failed/done) and a structured error.
- **Safe against plugin failure:** a plugin crash or hang during render fails or bypasses deterministically, per the documented policy.
  It never hangs the job forever.
- **Output integrity:** write to a temp file, then fsync and rename atomically. Correct headers and length. Dither and format are applied once.
  Offline output matches realtime output for the same project (null test within a documented tolerance).
- Tests: cancel mid-render, plugin crash mid-render, disk full, and comparing offline vs realtime output (`/failure-test render`).
