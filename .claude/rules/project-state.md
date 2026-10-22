---
paths:
  - "**/project/**"
  - "**/document/**"
  - "**/model/**"
  - "**/serializ*/**"
  - "**/persist*/**"
  - "**/undo/**"
---
# Project document / state rules
<!-- Globs are provisional until the directory layout is decided. -->

- The document model is owned by the main thread. The audio engine receives immutable compiled snapshots, never live references.
- Every mutation goes through the undo/command system. There are no silent edits.
- The file format is versioned. Loading an older version migrates it; loading a newer or unknown version fails clearly, never by guessing.
- Saving is atomic (temp file, fsync, rename). Autosave never blocks the UI or audio thread.
- Loading untrusted project files: validate every size, index and reference, so a malformed file cannot crash or allocate unboundedly.
- Round-trip test for every new field: save → load → save produces identical bytes or an equal model.
