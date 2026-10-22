---
paths:
  - "**/audio/**"
  - "**/engine/**"
  - "**/realtime/**"
  - "**/rt/**"
  - "**/dsp/**"
  - "**/graph/**"
---
# Audio realtime rules
<!-- Globs are provisional until the directory layout is decided (NEXT_ACTIONS #2). -->

Code reachable from the audio callback must be wait-free or bounded lock-free. It must never:
- allocate or free (`new`, `delete`, `malloc`, growing `std::vector`/`std::string`, `std::function` captures that allocate, `shared_ptr` last-release)
- take a mutex or any unbounded lock, wait on a condition variable, or sleep
- do disk, network or database I/O; open files; blocking IPC; syscalls with unbounded latency
- log through formatted or I/O loggers (push fixed-size records to a lock-free ring buffer instead)
- run AI inference, scan plugins, encode or decode files, or throw exceptions

When changing a realtime path, state in the PR or commit:
1. **Deadline:** the worst-case cost per block at the smallest supported buffer size and the highest sample rate.
2. **Allocation:** where memory is preallocated, and where it is reclaimed (never on the audio thread).
3. **Locking:** which atomics and memory orders are used, and why they are sufficient.
4. **Thread ownership:** who owns each touched object, and how ownership is handed over.
5. **Cache behavior:** data layout, and no pointer-chasing in hot loops.
6. **Dropout risk:** what happens on overrun (must degrade, never block).

Prove it with a test where possible: an allocation-counting hook and a lock-detection hook around the callback, and a stress test at small buffer sizes.
Run `/realtime-review` on the diff.
