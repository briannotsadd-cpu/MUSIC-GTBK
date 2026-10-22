# Next Actions

> Ordered queue. Top item = what the next session works on. Remove items when done (record the outcome in PROJECT_STATE.md).
> Feature freeze is active: only infrastructure and decision items below are allowed.

0. **[owner input] Tell Claude where the Nova Obsidian vault is** (absolute path on a machine Claude can reach, e.g. a local session or a git repo),
   and set `NOVA_VAULT_PATH` in `.claude/settings.local.json`. No vault was found in the cloud session. Until then, `/obsidian-sync` leaves notes pending.
1. **[P0, owner decision] Choose the stack.** Answer the open questions in `ARCHITECTURE.md` §Open questions
   (`architect` + `researcher` agents can prepare an options memo; the owner decides). Record in `DECISIONS.md`.
2. **[P0] Fix the directory layout.** Then tighten the `paths:` globs in `.claude/rules/*.md` to the real directories,
   and fill in CLAUDE.md §Stack and layout.
3. **[P1] Build skeleton.** Add the build system, formatter config (`.clang-format` if C++), a unit-test framework and one passing test.
   Done when `scripts/verify.sh fast` exits 0 and `full` exits 0 with sanitizers.
4. **[P1] CI.** Run `scripts/verify.sh full` on push.
5. **[P2] Realtime engine skeleton** with tests proving no allocation or locking on the audio thread
   (e.g. allocation-counting hook in tests). Blocked by the feature freeze until the owner lifts it.
