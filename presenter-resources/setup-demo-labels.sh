#!/usr/bin/env bash
# setup-demo-labels.sh — Create the labels required by app_final.py / app.py
#
# 本番デモ前に、コメント投稿先リポジトリで 1 回だけ実行してください。
# Run this once against the repo you will post analyses to.
#
# app_final.py の SKILL_LABELS は以下の GitHub ラベルを add_labels で付与しようとします。
# これらが対象リポジトリに存在しないと GitHub API は 422 を返し、デモ中にラベルが付きません。
#
# Required labels (matching SKILL_LABELS in app_final.py):
#   - good first issue       (built-in)
#   - difficulty: easy       (junior)
#   - difficulty: medium     (mid-level)
#   - difficulty: hard       (senior)
#   - difficulty: expert     (senior+)
#
# Usage:
#   bash presenter-resources/setup-demo-labels.sh <owner>/<repo>
#
# Example:
#   bash presenter-resources/setup-demo-labels.sh ChibaYuki347/demo_project_with_issues

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <owner>/<repo>" >&2
  echo "Example: $0 ChibaYuki347/demo_project_with_issues" >&2
  exit 1
fi

REPO="$1"

if ! command -v gh >/dev/null 2>&1; then
  echo "✗ gh CLI is not installed. Install from https://cli.github.com/" >&2
  exit 1
fi

echo "→ Creating skill-level labels in ${REPO}..."

# Color palette (GitHub label colors, no leading #):
# easy   = green   (#0e8a16)
# medium = yellow  (#fbca04)
# hard   = orange  (#d93f0b)
# expert = red     (#b60205)
declare -A LABELS=(
  ["difficulty: easy"]="0e8a16|Junior — good first issue / 初学者向け"
  ["difficulty: medium"]="fbca04|Mid-level developer / 中級者向け"
  ["difficulty: hard"]="d93f0b|Senior developer / 上級者向け"
  ["difficulty: expert"]="b60205|Senior+ / team effort / 専門家・チーム対応"
)

for name in "${!LABELS[@]}"; do
  IFS='|' read -r color desc <<<"${LABELS[$name]}"
  if gh label create "$name" -R "$REPO" --color "$color" --description "$desc" 2>/dev/null; then
    echo "  ✓ created: $name"
  else
    # Already exists → update color/description to match
    if gh label edit "$name" -R "$REPO" --color "$color" --description "$desc" >/dev/null 2>&1; then
      echo "  ✓ updated: $name"
    else
      echo "  ⚠️  skipped: $name (could not create or update)" >&2
    fi
  fi
done

# good first issue is a built-in label that GitHub usually pre-creates.
# Re-create it defensively in case it was deleted.
if ! gh label list -R "$REPO" | grep -q '^good first issue'; then
  gh label create "good first issue" -R "$REPO" --color "7057ff" --description "Good for newcomers" \
    && echo "  ✓ created: good first issue" \
    || echo "  ⚠️  could not create 'good first issue'" >&2
fi

echo ""
echo "✓ Done. Verify with: gh label list -R ${REPO}"
