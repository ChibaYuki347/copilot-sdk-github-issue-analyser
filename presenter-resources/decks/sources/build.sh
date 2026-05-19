#!/usr/bin/env bash
# build.sh — Generate 4 variants of the deck (JA/EN × light/dark).
#
# Output: presenter-resources/decks/AI_Genius_Copilot_SDK_Ep3_<LANG>_<MODE>.{pptx,pdf}
#
# Requirements:
#   - Node.js 18+ (for pptxgenjs)
#   - LibreOffice (for PPTX → PDF conversion)
#   - microsoft-brand-guidelines skill at ~/.copilot/skills/microsoft-brand-guidelines

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DECKS_DIR="$(dirname "$SCRIPT_DIR")"
BRAND_SKILL="${BRAND_SKILL:-$HOME/.copilot/skills/microsoft-brand-guidelines}"
RUNNER="$BRAND_SKILL/examples/deck-from-json.js"

if [ ! -f "$RUNNER" ]; then
  echo "❌ Brand skill runner not found at: $RUNNER" >&2
  echo "   Set BRAND_SKILL=/path/to/microsoft-brand-guidelines and retry." >&2
  exit 1
fi

# Make sure pptxgenjs is installed in the brand skill folder
if [ ! -d "$BRAND_SKILL/node_modules/pptxgenjs" ]; then
  echo "📦 Installing pptxgenjs in $BRAND_SKILL ..."
  (cd "$BRAND_SKILL" && [ -f package.json ] || echo '{"name":"ms-brand","private":true}' > package.json)
  (cd "$BRAND_SKILL" && npm install pptxgenjs --no-audit --no-fund --silent)
fi

PAIRS=(
  "ja-light  AI_Genius_Copilot_SDK_Ep3_JA_light"
  "ja-dark   AI_Genius_Copilot_SDK_Ep3_JA_dark"
  "en-light  AI_Genius_Copilot_SDK_Ep3_EN_light"
  "en-dark   AI_Genius_Copilot_SDK_Ep3_EN_dark"
)

cd "$SCRIPT_DIR"

for pair in "${PAIRS[@]}"; do
  read -r src out <<<"$pair"
  src_file="slides-${src}.json"
  pptx_out="$DECKS_DIR/${out}.pptx"
  pdf_out="$DECKS_DIR/${out}.pdf"
  echo ""
  echo "▶ Building $src_file → ${out}.{pptx,pdf}"
  if [ ! -f "$src_file" ]; then
    echo "  ⚠️  Source not found: $src_file (skipped)"
    continue
  fi
  node "$RUNNER" "$src_file" "$pptx_out"
  libreoffice --headless --convert-to pdf --outdir "$DECKS_DIR" "$pptx_out" >/dev/null
  echo "  ✓ $(basename "$pptx_out") ($(stat -c%s "$pptx_out") bytes)"
  echo "  ✓ $(basename "$pdf_out")  ($(stat -c%s "$pdf_out") bytes)"
done

echo ""
echo "🎉 Done. Outputs in $DECKS_DIR/"
ls -la "$DECKS_DIR"/*.pptx "$DECKS_DIR"/*.pdf 2>/dev/null | awk '{print "   "$NF" ("$5" bytes)"}'
