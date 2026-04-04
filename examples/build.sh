#!/usr/bin/env bash
# =============================================================================
# build.sh — build MaTiSSe example presentations
#
# Usage (from the repository root):
#   examples/build.sh                  # build all examples
#   examples/build.sh getting-started  # build one example by name
#   examples/build.sh --list           # list available example names
#   examples/build.sh --help           # show this help
#
# Available examples:
#   getting-started    impress.js feature tour (original getting-started talk)
#   reveal-quickstart  minimal reveal.js presentation with speaker notes
#   reveal-scientific  14-slide CFD conference talk (reveal.js)
#   themes/beamer-antibes    built-in theme: triple header, navy/white
#   themes/beamer-berkely    built-in theme: left sidebar + header, blue/white
#   themes/beamer-berlin     built-in theme: triple header + footer, navy/white
#   themes/beamer-madrid     built-in theme: header + rich footer, blue/white
#   themes/matisse           built-in theme: right sidebar + header + footer
#   themes/sapienza          built-in theme: header + footer, crimson/white
#   themes/solarized-dark    built-in theme: left sidebar + header + footer, solarized dark
#   themes/dracula           built-in theme: left sidebar + header + footer, dracula dark
# =============================================================================
set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration — add / edit entries here to register new examples
# Each entry: "name|matisse-command"
# The name is what the user passes on the command line.
# The command is run from the repository root (no leading 'matisse build').
# ---------------------------------------------------------------------------
declare -a EXAMPLES=(
  "getting-started|-i examples/getting-started/getting_started.md -o examples/getting-started/out/ --toc-at-subsec-beginning 2"
  "reveal-quickstart|-i examples/reveal-quickstart/quickstart.md -o examples/reveal-quickstart/out/ --backend reveal"
  "reveal-scientific|-i examples/reveal-scientific/talk.md -o examples/reveal-scientific/out/ --backend reveal"
  "themes/beamer-antibes|-i examples/themes/talk.md -o examples/themes/beamer-antibes/out/ --theme beamer-antibes"
  "themes/beamer-berkely|-i examples/themes/talk.md -o examples/themes/beamer-berkely/out/ --theme beamer-berkely"
  "themes/beamer-berlin|-i examples/themes/talk.md -o examples/themes/beamer-berlin/out/ --theme beamer-berlin"
  "themes/beamer-madrid|-i examples/themes/talk.md -o examples/themes/beamer-madrid/out/ --theme beamer-madrid"
  "themes/matisse|-i examples/themes/talk.md -o examples/themes/matisse/out/ --theme matisse"
  "themes/sapienza|-i examples/themes/talk.md -o examples/themes/sapienza/out/ --theme sapienza"
  "themes/solarized-dark|-i examples/themes/talk.md -o examples/themes/solarized-dark/out/ --theme solarized-dark"
  "themes/dracula|-i examples/themes/talk.md -o examples/themes/dracula/out/ --theme dracula"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_names() {
  for entry in "${EXAMPLES[@]}"; do
    echo "${entry%%|*}"
  done
}

_cmd_for() {
  local target="$1"
  for entry in "${EXAMPLES[@]}"; do
    local name="${entry%%|*}"
    local cmd="${entry#*|}"
    if [[ "$name" == "$target" ]]; then
      echo "$cmd"
      return 0
    fi
  done
  return 1
}

_build_one() {
  local name="$1"
  local cmd
  if ! cmd="$(_cmd_for "$name")"; then
    echo "ERROR: unknown example '$name'" >&2
    echo "Run 'examples/build.sh --list' to see available names." >&2
    exit 1
  fi
  echo "──────────────────────────────────────────"
  echo "Building: $name"
  echo "  matisse build $cmd"
  echo "──────────────────────────────────────────"
  # shellcheck disable=SC2086
  matisse build --offline $cmd
  echo "✓ $name → done"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
case "${1:-}" in
  --help|-h)
    sed -n '2,/^# ===*/p' "$0" | grep '^#' | sed 's/^# \{0,1\}//'
    exit 0
    ;;
  --list|-l)
    echo "Available examples:"
    _names | sed 's/^/  /'
    exit 0
    ;;
  "")
    # Build all
    ok=0; fail=0
    for name in $(_names); do
      if _build_one "$name"; then
        (( ok++ )) || true
      else
        (( fail++ )) || true
      fi
    done
    echo ""
    echo "Results: ${ok} succeeded, ${fail} failed"
    [[ $fail -eq 0 ]]
    ;;
  *)
    _build_one "$1"
    ;;
esac
