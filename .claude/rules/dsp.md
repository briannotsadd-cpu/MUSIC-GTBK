---
paths:
  - "**/dsp/**"
  - "**/effects/**"
  - "**/fx/**"
  - "**/synth/**"
  - "**/filters/**"
---
# DSP rules
<!-- Globs are provisional until the directory layout is decided. -->

Every DSP change needs tests covering:
- sample rates: 44.1k, 48k, 88.2k, 96k, 192k (and any coefficient recomputation on change)
- channel layouts: mono, stereo, and multichannel if supported; mismatched in/out counts
- input signals: silence (output stays silent and denormal-free), unit impulse (expected impulse response), DC, full-scale sine, white noise
- NaN/Inf input (must not propagate or latch the state; define the policy: sanitize or reset)
- denormals: decaying tails with FTZ/DAZ set, and verify they are not needed for correctness
- extreme parameters: min, max, and jumps between them in one block (no blow-ups or clicks; smoothing where audible)
- automation: sample-accurate or block-accurate as documented, ramps across block boundaries
- reset/prepare: same output after `reset()` as from a fresh instance

Constants: every non-obvious number gets a comment with its DSP derivation or source (e.g. "−3 dB = 0.7071").
Arbitrary tuning constants with no reason are rejected.
Prefer double precision for coefficient design. Document the precision used in the processing loop.
Latency introduced by a processor must be reported to the host for compensation.
