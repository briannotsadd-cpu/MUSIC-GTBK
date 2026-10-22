#!/usr/bin/env bash
# Nova verification entry point.
#   scripts/verify.sh fast          format check (changed files) + build + `unit` tests
#   scripts/verify.sh full          format check (all) + ASan/UBSan build + all tests + TSan build + all tests
#   scripts/verify.sh --state-hash  print the hash of the working tree's changes (used by the Stop hook)
# Exit codes: 0 = checks ran and passed, 1 = a check failed, 2 = usage error, 3 = nothing verifiable (NOT a pass).
# On 0/1 the result is stamped in .claude/state/last-verify so hooks can tell whether the current diff was verified.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 2
STATE_DIR="$ROOT/.claude/state"
JOBS="$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 4)"

if command -v sha1sum >/dev/null; then SHA=(sha1sum); else SHA=(shasum -a 1); fi  # macOS has only shasum

state_hash() {
  {
    git rev-parse HEAD 2>/dev/null || echo "no-head"
    git diff HEAD --binary 2>/dev/null
    git ls-files --others --exclude-standard -z 2>/dev/null |
      while IFS= read -r -d '' f; do printf '%s ' "$f"; "${SHA[@]}" < "$f"; done
  } | "${SHA[@]}" | cut -d' ' -f1
}

stamp() { # $1=mode $2=result
  mkdir -p "$STATE_DIR"
  printf '%s %s %s %s\n' "$1" "$2" "$(state_hash)" "$(date -u +%FT%TZ)" > "$STATE_DIR/last-verify"
}

step() { printf '\n== %s\n' "$*"; }
fail() { printf '\nVERIFY FAILED: %s\n' "$*"; stamp "$MODE" fail; exit 1; }

cxx_files() { # $1=changed|all
  local pat='\.(c|cc|cpp|cxx|h|hh|hpp|hxx|mm)$'
  if [ "$1" = changed ]; then
    { git diff HEAD --name-only --diff-filter=d; git ls-files --others --exclude-standard; } | grep -E "$pat" | sort -u
  else
    git ls-files | grep -E "$pat"
  fi
}

format_check() { # $1=changed|all
  if [ ! -f .clang-format ]; then echo "skip: no .clang-format"; return 0; fi
  command -v clang-format >/dev/null || fail "clang-format not installed"
  local files; files="$(cxx_files "$1")"
  [ -z "$files" ] && { echo "no C/C++ files to check"; return 0; }
  echo "$files" | xargs clang-format --dry-run -Werror || fail "formatting (run clang-format -i on the files above)"
}

cmake_build_test() { # $1=build-dir $2=ctest-label-regex-or-empty $3...=extra cmake args
  local dir="$1" label="$2"; shift 2
  local gen=(); command -v ninja >/dev/null && gen=(-G Ninja)
  cmake -S . -B "$dir" ${gen[@]+"${gen[@]}"} -DCMAKE_EXPORT_COMPILE_COMMANDS=ON "$@" >/dev/null || fail "cmake configure ($dir)"
  cmake --build "$dir" -j "$JOBS" || fail "build ($dir)"
  local args=(--test-dir "$dir" --output-on-failure -j "$JOBS" --no-tests=error)
  [ -n "$label" ] && args+=(-L "$label")
  ctest "${args[@]}" || fail "tests ($dir${label:+, label $label})"
}

MODE="${1:-}"
case "$MODE" in
  --state-hash) state_hash; exit 0 ;;
  fast|full) ;;
  *) echo "usage: scripts/verify.sh fast|full|--state-hash" >&2; exit 2 ;;
esac

if [ ! -f CMakeLists.txt ]; then
  # Extension point: when the stack is chosen (DECISIONS.md), add its detection and commands here.
  echo "NOTHING VERIFIED: no build system found (no CMakeLists.txt). Project is pre-code — see PROJECT_STATE.md."
  exit 3
fi

if [ "$MODE" = fast ]; then
  step "format (changed files)"; format_check changed
  step "build + unit tests"; cmake_build_test build/fast unit -DCMAKE_BUILD_TYPE=Debug
else
  step "format (all files)"; format_check all
  step "ASan+UBSan build + all tests"
  cmake_build_test build/asan "" -DCMAKE_BUILD_TYPE=Debug \
    "-DCMAKE_CXX_FLAGS=-fsanitize=address,undefined -fno-omit-frame-pointer -fno-sanitize-recover=all" \
    "-DCMAKE_C_FLAGS=-fsanitize=address,undefined -fno-omit-frame-pointer -fno-sanitize-recover=all"
  step "TSan build + all tests"
  cmake_build_test build/tsan "" -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    "-DCMAKE_CXX_FLAGS=-fsanitize=thread -fno-omit-frame-pointer" \
    "-DCMAKE_C_FLAGS=-fsanitize=thread -fno-omit-frame-pointer"
fi

stamp "$MODE" pass
printf '\nVERIFY PASSED (%s)\n' "$MODE"
