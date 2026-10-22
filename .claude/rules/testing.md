---
paths:
  - "**/test/**"
  - "**/tests/**"
  - "**/*_test.*"
  - "**/*Test.*"
  - "**/*.test.*"
  - "**/bench*/**"
---
# Testing rules

- A test must fail if the behavior it covers breaks. Before calling a test meaningful, check it fails against the broken code (or a mutated copy).
- Never weaken, skip or delete a test to get green. Fix the code or report the failure.
- Tag tests with labels so `scripts/verify.sh` can select them: `unit` (fast), `dsp`, `plugin`, `render`, `stress`, `integration`.
- Determinism: fixed seeds, no wall-clock sleeps for synchronization, no dependence on real audio devices in unit tests (use a fake device driving the callback).
- Numeric comparisons use explicit, justified tolerances (e.g. "−120 dBFS null").
- Every bug fix adds a regression test that reproduces the original failure.
