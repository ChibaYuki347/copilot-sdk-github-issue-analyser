#!/bin/bash

# Pre-Livestream Test Script
# Run this to verify everything is ready to go

set -e

echo "🎬 GitHub Issue Complexity Analyser — Pre-Stream Test"
echo "=========================================================\n"

# Prefer the project virtualenv interpreter so checks match installed deps.
if [ -x ".venv/bin/python" ]; then
    PYTHON_BIN=".venv/bin/python"
else
    PYTHON_BIN="python3"
fi

# Check Python
echo "✅ Checking Python..."
"$PYTHON_BIN" --version

# Check dependencies
echo "\n✅ Checking dependencies..."
"$PYTHON_BIN" -c "import copilot; print(f'Copilot SDK: ✓')"
"$PYTHON_BIN" -c "import fastapi; print(f'FastAPI: ✓')"
"$PYTHON_BIN" -c "import pydantic; print(f'Pydantic: ✓')"
"$PYTHON_BIN" -c "import httpx; print(f'httpx: ✓')"

# Check GitHub token
echo "\n✅ Checking GITHUB_TOKEN..."
if [ -f ".env" ]; then
    set +e
    . ./.env
    set -e
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  GITHUB_TOKEN not set"
    echo "   Create a token at: https://github.com/settings/tokens?type=beta"
    echo "   Then add to .env file: GITHUB_TOKEN=ghp_..."
else
    echo "   Token is set (${#GITHUB_TOKEN} chars)"
fi

# Check Copilot CLI
echo "\n✅ Checking Copilot CLI..."
if gh copilot --help > /dev/null 2>&1; then
    gh --version | head -1
    echo "gh copilot: ✓"
elif command -v copilot > /dev/null 2>&1; then
    copilot --version
else
    echo "⚠️  Copilot CLI not found. Install with: gh extension install github/gh-copilot"
fi

# Test Phase 2a: Hello World
echo "\n✅ Testing Phase 2a: Hello World (send_and_wait)..."
set +e
PHASE2A_OUTPUT=$(timeout 30 "$PYTHON_BIN" app.py hello 2>&1)
PHASE2A_STATUS=$?
set -e
printf "%s\n" "$PHASE2A_OUTPUT" | head -5
if [ "$PHASE2A_STATUS" -eq 0 ]; then
    echo "   ✓ Phase 2a works!"
else
    echo "   ⚠️  Phase 2a failed"
fi

# Test Phase 2b: Streaming
echo "\n✅ Testing Phase 2b: Hello World (streaming)..."
set +e
PHASE2B_OUTPUT=$(timeout 30 "$PYTHON_BIN" app.py hello-stream 2>&1)
PHASE2B_STATUS=$?
set -e
printf "%s\n" "$PHASE2B_OUTPUT" | head -5
if [ "$PHASE2B_STATUS" -eq 0 ]; then
    echo "   ✓ Phase 2b works!"
else
    echo "   ⚠️  Phase 2b failed"
fi

echo "\n=========================================================\n"
echo "✅ Pre-Stream Test Complete!"
echo ""
echo "📌 Next Steps:"
echo "   1. Prepare 2-3 GitHub issue URLs to test"
echo "   2. Test CLI analysis: python app.py <issue_url>"
echo "   3. Test web UI: python app.py serve (then open http://localhost:8000)"
echo "   4. Review deck (AI_Genius_Copilot_SDK_Ep3_EN.pdf) and script.md"
echo "   5. Do a dry run of the full 60-minute build"
echo ""
echo "🚀 You're ready to stream!"
