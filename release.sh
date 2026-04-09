#!/usr/bin/env bash
# release.sh — Bump MaTiSSe.py version, generate changelog, publish to GitHub.
#
# Usage:
#   ./release.sh (--major | --minor | --patch | <X.Y.Z>)
#
#   --major, -M     X.Y.Z → X+1.0.0
#   --minor, -m     X.Y.Z → X.Y+1.0
#   --patch, -p     X.Y.Z → X.Y.Z+1
#   <X.Y.Z>         set an explicit version

set -euo pipefail

MATISSE_INIT="matisse/__init__.py"

die()  { echo "ERROR: $*" >&2; exit 1; }
info() { echo "==> $*"; }

usage() {
  sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'
  exit 1
}

current_version() {
  grep -oP '(?<=__version__ = ")[^"]+' "$MATISSE_INIT"
}

bump() {
  local cur="$1" part="$2"
  local major minor patch
  IFS='.' read -r major minor patch <<< "$cur"
  case "$part" in
    major) echo "$((major + 1)).0.0" ;;
    minor) echo "${major}.$((minor + 1)).0" ;;
    patch) echo "${major}.${minor}.$((patch + 1))" ;;
  esac
}

# ── stage tracking + recovery trap ───────────────────────────────────────────
STAGE="preflight"
RELEASE_BRANCH=""
NEW_VER=""

on_error() {
  echo ""
  echo "================================================================"
  echo "  release.sh FAILED at stage: $STAGE"
  echo "================================================================"
  case "$STAGE" in
    preflight | lint | confirm)
      echo "  Nothing was changed. Fix the issue above and re-run:"
      echo "    ./release.sh $*"
      ;;
    branched | tests)
      echo "  The release branch '$RELEASE_BRANCH' was created but nothing"
      echo "  was committed yet. To clean up and start over:"
      echo "    git checkout develop"
      echo "    git branch -D $RELEASE_BRANCH"
      echo "  Then fix the issue above and re-run:"
      echo "    ./release.sh $*"
      ;;
    committed)
      echo "  The release branch '$RELEASE_BRANCH' has the version-bump commit."
      echo "  To clean up and start over:"
      echo "    git checkout develop"
      echo "    git branch -D $RELEASE_BRANCH"
      echo "  Or to resume manually from here:"
      echo "    git checkout master"
      echo "    git pull origin master --ff-only"
      echo "    git merge --no-ff $RELEASE_BRANCH -m \"Merge branch '$RELEASE_BRANCH'\""
      echo "    git tag -a v${NEW_VER} -m \"Release v${NEW_VER}\""
      echo "    git push origin master"
      echo "    git push origin v${NEW_VER}"
      echo "    git checkout develop"
      echo "    git merge --no-ff master -m 'Merge branch master into develop'"
      echo "    git push origin develop"
      echo "    git branch -d $RELEASE_BRANCH"
      ;;
    merged | tagged)
      echo "  master has been merged/tagged locally but not yet pushed."
      echo "  To resume:"
      echo "    git push origin master"
      echo "    git push origin v${NEW_VER}"
      echo "    git checkout develop"
      echo "    git merge --no-ff master -m 'Merge branch master into develop'"
      echo "    git push origin develop"
      echo "    git branch -d $RELEASE_BRANCH"
      ;;
    pushed_master)
      echo "  master was pushed but the tag was not. To resume:"
      echo "    git push origin v${NEW_VER}"
      echo "    git checkout develop"
      echo "    git merge --no-ff master -m 'Merge branch master into develop'"
      echo "    git push origin develop"
      echo "    git branch -d $RELEASE_BRANCH"
      ;;
    pushed_tag)
      echo "  Tag v${NEW_VER} was pushed (CI/PyPI triggered). Still need to:"
      echo "    git checkout develop"
      echo "    git merge --no-ff master -m 'Merge branch master into develop'"
      echo "    git push origin develop"
      echo "    git branch -d $RELEASE_BRANCH"
      ;;
    merged_develop)
      echo "  develop was merged locally but not pushed. To resume:"
      echo "    git push origin develop"
      echo "    git branch -d $RELEASE_BRANCH"
      ;;
  esac
  echo "================================================================"
}

trap 'on_error "$@"' ERR

# ── argument parsing ──────────────────────────────────────────────────────────
[[ $# -ge 1 ]] || usage

BUMP_ARG=""

for arg in "$@"; do
  case "$arg" in
    --major | -M)           BUMP_ARG=major ;;
    --minor | -m)           BUMP_ARG=minor ;;
    --patch | -p)           BUMP_ARG=patch ;;
    [0-9]*.[0-9]*.[0-9]*)  BUMP_ARG="$arg" ;;
    *) usage ;;
  esac
done

[[ -n "$BUMP_ARG" ]] || usage

CUR_VER=$(current_version)
case "$BUMP_ARG" in
  major | minor | patch) NEW_VER=$(bump "$CUR_VER" "$BUMP_ARG") ;;
  *)                     NEW_VER="$BUMP_ARG" ;;
esac

RELEASE_BRANCH="release/v${NEW_VER}"

# ── pre-flight checks ─────────────────────────────────────────────────────────
STAGE="preflight"
[[ -f "$MATISSE_INIT" ]]        || die "$MATISSE_INIT not found — run from the repo root"
command -v git-cliff >/dev/null || die "'git-cliff' not found (install: pipx install git-cliff)"

CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || true)
[[ "$CURRENT_BRANCH" == "develop" ]] \
  || die "must be on 'develop' branch (currently on '$CURRENT_BRANCH')"
[[ -z "$(git status --porcelain)" ]] \
  || die "working tree is not clean — commit or stash changes first"

git fetch --tags --quiet
[[ -z "$(git tag -l "v${NEW_VER}")" ]] || die "tag v${NEW_VER} already exists"

DEVELOP_BEHIND=$(git rev-list --count HEAD..origin/develop 2>/dev/null || echo 0)
MASTER_BEHIND=$(git rev-list --count master..origin/master 2>/dev/null || echo 0)
[[ "$DEVELOP_BEHIND" -eq 0 ]] || die "develop is ${DEVELOP_BEHIND} commit(s) behind origin/develop — run: git pull origin develop"
[[ "$MASTER_BEHIND"  -eq 0 ]] || die "master is ${MASTER_BEHIND} commit(s) behind origin/master — run: git pull origin master"

# ── lint / format check (before any branch is created) ───────────────────────
STAGE="lint"
info "Running ruff lint + format check"
ruff check matisse/ tests/ || die "lint failed — run 'make fmt' to fix, then retry"
ruff format --check matisse/ tests/ || die "format check failed — run 'make fmt' to fix, then retry"

# ── confirm ───────────────────────────────────────────────────────────────────
STAGE="confirm"
echo "  Current version : $CUR_VER"
echo "  New version     : $NEW_VER"
echo
read -r -p "Proceed? [y/N] " confirm
[[ "$confirm" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }

# ── create release branch ─────────────────────────────────────────────────────
STAGE="branched"
info "Creating branch $RELEASE_BRANCH"
git checkout -b "$RELEASE_BRANCH"

# ── bump version ──────────────────────────────────────────────────────────────
info "Bumping version ($CUR_VER → $NEW_VER)"
sed -i "s/__version__ = \"${CUR_VER}\"/__version__ = \"${NEW_VER}\"/" "$MATISSE_INIT"

# ── generate changelog ────────────────────────────────────────────────────────
info "Generating docs/guide/changelog.md with git-cliff"
mkdir -p docs/guide
git-cliff --tag "v${NEW_VER}" -o docs/guide/changelog.md

# ── run tests ─────────────────────────────────────────────────────────────────
STAGE="tests"
info "Running test suite"
python -m pytest

# ── commit release ────────────────────────────────────────────────────────────
STAGE="committed"
git add "$MATISSE_INIT" docs/guide/changelog.md
git commit -m "chore(release): bump version to v${NEW_VER}"

# ── merge to master, tag, push ────────────────────────────────────────────────
STAGE="merged"
info "Merging to master and tagging v${NEW_VER}"
git checkout master
git pull origin master --ff-only
git merge --no-ff "$RELEASE_BRANCH" -m "Merge branch '${RELEASE_BRANCH}'"

STAGE="tagged"
git tag -a "v${NEW_VER}" -m "Release v${NEW_VER}"

STAGE="pushed_master"
info "Pushing master + tag to origin"
git push origin master

STAGE="pushed_tag"
git push origin "v${NEW_VER}"

# ── merge back to develop, push ───────────────────────────────────────────────
STAGE="merged_develop"
info "Merging master back to develop"
git checkout develop
git merge --no-ff master -m "Merge branch 'master' into develop"
git push origin develop

# ── remove local release branch ───────────────────────────────────────────────
git branch -d "$RELEASE_BRANCH"

# ── PyPI upload is triggered by the tag push via CI ───────────────────────────
info "Done — v${NEW_VER} released (PyPI upload triggered by tag push via CI)"
