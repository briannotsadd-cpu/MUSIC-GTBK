#!/usr/bin/env python3
"""Claude Code hooks for Nova. One entry point, one subcommand per hook event.

  session-start   SessionStart: short project status; on source=compact adds the recovery protocol
  guard-bash      PreToolUse(Bash): deny or ask for destructive shell/git commands
  post-edit       PostToolUse(Edit|Write): fast per-file checks (clang-format, realtime red flags)
  stop-gate       Stop: one reminder if source changed since the last scripts/verify.sh run

Hooks must be fast and must never crash the session: any unexpected error exits 0 silently.
This is a guardrail against accidents, not a security boundary.
"""
import json
import os
import re
import shlex
import subprocess
import sys

ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
SOURCE_EXT = re.compile(r"\.(c|cc|cpp|cxx|h|hh|hpp|hxx|mm|m|rs|swift)$")
REALTIME_DIRS = re.compile(r"(^|/)(audio|engine|realtime|rt|dsp|graph|effects|fx|synth|filters)/")


def run(args, timeout=5):
    try:
        out = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        return out.returncode, out.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return 1, ""


def emit(obj):
    print(json.dumps(obj))
    sys.exit(0)


def read_file(rel, max_lines):
    """First max_lines content lines, skipping headings, blockquote notes and blanks."""
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            lines = [l.rstrip() for l in f if l.strip() and not l.lstrip().startswith(("#", ">"))]
        return "\n".join(lines[:max_lines])
    except OSError:
        return f"({rel} missing)"


def verify_state():
    """Return (stamp_line or None, matches_current_tree)."""
    try:
        with open(os.path.join(ROOT, ".claude/state/last-verify"), encoding="utf-8") as f:
            stamp = f.read().strip()
    except OSError:
        return None, False
    code, current = run(["bash", "scripts/verify.sh", "--state-hash"], timeout=10)
    parts = stamp.split()
    return stamp, code == 0 and len(parts) >= 3 and parts[2] == current


# ---------------------------------------------------------------- SessionStart
def session_start(data):
    _, branch = run(["git", "branch", "--show-current"])
    _, dirty = run(["git", "status", "--short"])
    _, log = run(["git", "log", "--oneline", "-3"])
    stamp, fresh = verify_state()
    dirty_lines = dirty.splitlines()
    lines = [
        "[nova] Project status (from hooks; details in PROJECT_STATE.md):",
        f"branch: {branch or '?'} | uncommitted files: {len(dirty_lines)}",
        *[f"  {l}" for l in dirty_lines[:10]],
        *(["  ..."] if len(dirty_lines) > 10 else []),
        "recent commits:", *[f"  {l}" for l in log.splitlines()],
        f"last verify: {stamp or 'never'}{' (matches current tree)' if fresh else ' (stale or none)'}",
        "NEXT_ACTIONS.md (top):",
        read_file("NEXT_ACTIONS.md", 12),
    ]
    if data.get("source") == "compact":
        lines += [
            "",
            "[nova] CONTEXT WAS COMPACTED. Do not restart work from memory. Recover first:",
            "1. Run /context-recovery (reads PROJECT_STATE.md, git diff, affected subsystem, runs relevant tests).",
            "2. The uncommitted files above are in-progress work. Read the diff before changing anything.",
            "3. Critical constraints: no alloc/lock/IO/logging/inference in the audio callback;",
            "   plugins are untrusted and run out of process; render is off the UI thread and cancelable;",
            "   no DONE/FIXED claim without test evidence (else 'IMPLEMENTED — NOT VERIFIED').",
            "4. Source of truth: CLAUDE.md table. Feature freeze may be active (PROJECT_STATE.md).",
        ]
    emit({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "\n".join(lines)}})


# ------------------------------------------------------------------ PreToolUse
DENY_RM_TARGETS = {"/", "/*", "~", "~/", "~/*", "$HOME", "${HOME}", ".", "./", "..", "../", "*", ".git", ".git/"}


def segments(cmd):
    for seg in re.split(r"&&|\|\||;|\||\n", cmd):
        try:
            toks = shlex.split(seg, posix=True)
        except ValueError:
            toks = seg.split()
        while toks and (toks[0] in ("sudo", "command", "exec", "env", "time") or "=" in toks[0]):
            toks = toks[1:]
        if toks:
            yield toks


def check_command(cmd):
    """Return (decision, reason) or None."""
    for t in segments(cmd):
        prog, args = os.path.basename(t[0]), t[1:]
        flags = "".join(a.lstrip("-") for a in args if a.startswith("-") and not a.startswith("--"))
        if prog == "rm" and ("r" in flags.lower() or "--recursive" in args):
            targets = [a for a in args if not a.startswith("-")]
            bad = [a for a in targets if a in DENY_RM_TARGETS or re.fullmatch(r"/[^/]*/?", a)]
            if bad:
                return "deny", f"Recursive rm on {bad} would destroy the repo or system. Remove specific paths instead."
        if prog != "git":
            continue
        while args and args[0] in ("-C", "-c", "--git-dir", "--work-tree"):  # skip git global options
            args = args[2:]
        if not args:
            continue
        sub, rest = args[0], args[1:]
        if sub == "push" and (any(a in ("--force", "-f") for a in rest) or any(a.startswith("+") for a in rest)):
            return "deny", "Force-push rewrites shared history. Use --force-with-lease on your own branch, and only with explicit permission."
        if sub == "push" and "--force-with-lease" in rest:
            return "ask", "Force-with-lease push: confirm the branch is yours and the user approved rewriting it."
        if sub == "reset" and "--hard" in rest:
            return "ask", "git reset --hard discards uncommitted work. Inspect `git status`/`git diff` first."
        if sub == "clean" and any(re.fullmatch(r"-[a-zA-Z]*f[a-zA-Z]*", a) or a == "--force" for a in rest):
            return "ask", "git clean -f deletes untracked files permanently."
        if sub in ("checkout", "restore") and "--staged" not in rest and any(a in (".", "--", ":/") for a in rest):
            return "ask", "This discards working-tree changes. Make sure they are not someone else's work."
        if sub == "branch" and ("-D" in rest or ("--delete" in rest and "--force" in rest)):
            return "ask", "Force-deleting a branch can lose unmerged commits."
        if sub == "stash" and rest[:1] in (["drop"], ["clear"]):
            return "ask", "Dropping stashes loses saved work."
        if sub in ("filter-branch", "filter-repo") or (sub == "rebase" and not set(rest) & {"--abort", "--continue", "--skip"}):
            return "ask", "History rewrite: confirm it is your own unpublished branch."
    return None


def guard_bash(data):
    cmd = (data.get("tool_input") or {}).get("command", "")
    hit = check_command(cmd)
    if hit:
        decision, reason = hit
        emit({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                     "permissionDecision": decision,
                                     "permissionDecisionReason": f"[nova guard] {reason}"}})
    sys.exit(0)


# ----------------------------------------------------------------- PostToolUse
RT_RED_FLAGS = [
    (r"\bnew\s+[A-Za-z_:]|\bdelete(\s*\[\])?\s+[A-Za-z_*(]|\b(malloc|calloc|realloc|free)\s*\(", "heap allocation/free"),
    (r"\.(push_back|emplace_back|resize|reserve|insert)\s*\(", "container growth (may allocate)"),
    (r"std::(mutex|recursive_mutex|shared_mutex|condition_variable|lock_guard|unique_lock|scoped_lock)", "blocking lock"),
    (r"\b(printf|fprintf|std::cout|std::cerr|NSLog|OutputDebugString|DBG)\b", "I/O logging"),
    (r"\b(fopen|ifstream|ofstream|std::filesystem|sleep|usleep|sleep_for|this_thread::sleep)\b", "file I/O or sleep"),
    (r"\bthrow\b", "exception throw"),
]


def post_edit(data):
    path = (data.get("tool_input") or {}).get("file_path", "")
    if not path or not SOURCE_EXT.search(path):
        sys.exit(0)
    rel = os.path.relpath(path, ROOT)
    notes = []
    if os.path.exists(os.path.join(ROOT, ".clang-format")) and re.search(r"\.(c|cc|cpp|cxx|h|hh|hpp|hxx|mm)$", path):
        code, _ = run(["clang-format", "--dry-run", "-Werror", path], timeout=10)
        if code != 0:
            notes.append(f"clang-format: {rel} is not formatted (run `clang-format -i {rel}`).")
    if REALTIME_DIRS.search("/" + rel.replace(os.sep, "/")):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            text = ""
        # Strip comments and string literals so prose ("a new idea") doesn't trigger flags.
        text = re.sub(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\\n])*"', " ", text, flags=re.S)
        found = sorted({label for pat, label in RT_RED_FLAGS if re.search(pat, text)})
        if found:
            notes.append(
                f"realtime check: {rel} is in a realtime directory and contains: {', '.join(found)}. "
                "Confirm none of it is reachable from the audio callback (see .claude/rules/audio-realtime.md). "
                "Heuristic only; false positives are expected in non-callback code.")
    if notes:
        emit({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "\n".join(notes)}})
    sys.exit(0)


# ------------------------------------------------------------------------ Stop
def stop_gate(data):
    if data.get("stop_hook_active"):
        sys.exit(0)  # remind once per stop, never loop
    _, changed = run(["git", "status", "--porcelain", "--untracked-files=all"])
    src = [l[3:] for l in changed.splitlines() if SOURCE_EXT.search(l)]
    if not src:
        sys.exit(0)
    _, fresh = verify_state()
    if fresh:
        sys.exit(0)
    emit({"decision": "block", "reason": (
        f"[nova] {len(src)} source file(s) changed and the current tree has not been through `scripts/verify.sh` "
        f"(e.g. {', '.join(src[:3])}). Either run `scripts/verify.sh fast` and report the result, "
        "or state explicitly that the change is IMPLEMENTED — NOT VERIFIED and why. "
        "Exit code 3 means nothing could be verified and is not a pass.")})


def main():
    try:
        data = json.load(sys.stdin)
    except (ValueError, OSError):
        data = {}
    handlers = {"session-start": session_start, "guard-bash": guard_bash,
                "post-edit": post_edit, "stop-gate": stop_gate}
    try:
        handlers[sys.argv[1]](data)
    except SystemExit:
        raise
    except Exception:  # never break the session because a hook had a bug
        sys.exit(0)


if __name__ == "__main__":
    main()
