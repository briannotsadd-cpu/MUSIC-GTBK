---
name: verify
description: Run Nova's verification (fast after small edits; full before claiming a major feature complete or before a release) and report the result with evidence. Use instead of ad-hoc build/test commands.
argument-hint: "fast|full|release"
---

# Verify: $ARGUMENTS (default: fast)

## Procedure
1. `git status --short`: note which files changed (this is what is being verified).
2. Run the mode:
   - **fast:** `scripts/verify.sh fast`
   - **full:** `scripts/verify.sh full`
   - **release:** `scripts/verify.sh full`, then the regression and release checks below.
3. Read the output. Keep only the failing section in context; do not paste full build logs.
   If the logs are huge, delegate reading them to a subagent.
4. On failure: report the first real error (file:line plus message), not cascading errors.
   Do not fix unrelated failures silently. List them.
5. **Regression (full/release):** for each bug fixed since the last release (`git log` messages with fix/regression),
   confirm a regression test exists and passed.
6. **Release (release only):** clean checkout build; version string bumped; `PROJECT_STATE.md` has no BROKEN P0;
   no `TODO(release)`; changelog entry present; the `/failure-test plugin` and `/failure-test render` results are recent.

## Exit codes
`0` pass · `1` fail · `3` NOTHING VERIFIED (no build system; this is not a pass).

## Output
```
VERIFY <mode>: PASS | FAIL | NOT VERIFIABLE
command → exit <n>
failures: <first error per failing step>
status claim allowed: VERIFIED (fast) | VERIFIED (full) | IMPLEMENTED — NOT VERIFIED
```

## Definition of Done
- The command ran in this session, and the real exit code is reported.
- The status claim matches the table in CLAUDE.md § Definition of Done.
  `fast` never justifies "production ready".
