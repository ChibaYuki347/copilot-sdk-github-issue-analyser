# Livestream Preparation Checklist

## ✅ What's Been Set Up For You

1. **`.env.example`** — Template for environment variables
2. **`.env`** — Ready for your GitHub token (created)
3. **`devcontainer.json`** — Now loads `.env` automatically when you create a Codespace
4. **`README.md`** — Updated with:
   - Token creation instructions
   - `.env` file setup  
   - Livestream presenter checklist
   - Troubleshooting guide
5. **`pre-stream-check.sh`** — Automated test script to verify everything works

## ⚠️ YOU STILL NEED TO DO (20 min)

### 1. Create a Fresh GitHub Token (5 min)

```
1. Go to: https://github.com/settings/tokens?type=beta
2. Click "Generate new token"
3. Name: "copilot-sdk-stream"
4. Expiration: 7 days
5. Repository access: All repositories
6. Permissions:
   - Issues: Read and Write ✓
   - Contents: Read ✓
7. Click "Generate token"
8. Copy the token (starts with ghp_)
```

### 2. Add Token to `.env` File (2 min)

Edit `.env` in the repo root:

```bash
# Open the file
open "/Users/reneenoble/Documents/Microsoft/Copilot SDK/AI Genius/copilot-sdk-github-issue-analyser-/.env"
```

Paste your token:

```
GITHUB_TOKEN=ghp_your_actual_token_here
```

Save and close.

### 3. Run Pre-Stream Test (5 min)

From the repo directory:

```bash
bash pre-stream-check.sh
```

This will verify:
- ✓ Python installation
- ✓ All dependencies installed
- ✓ GitHub token is set
- ✓ Copilot CLI works
- ✓ Phase 2a (send_and_wait) works
- ✓ Phase 2b (streaming) works

**Expected output:**
```
✅ GitHub Issue Complexity Analyser — Pre-Stream Test
=========================================================

✅ Checking Python...
Python 3.x.x

✅ Checking dependencies...
Copilot SDK: ✓
FastAPI: ✓
Pydantic: ✓
httpx: ✓

✅ Checking GITHUB_TOKEN...
   Token is set (50 chars)

... (test output) ...

✅ Pre-Stream Test Complete!
```

### 4. Prepare Test Issues (5 min)

Choose 2-3 GitHub issues to demo during the stream:

1. **Issue 1** (Simple):
   - URL: `https://github.com/...`
   - Expected complexity: Junior

2. **Issue 2** (Moderate):
   - URL: `https://github.com/...`
   - Expected complexity: Mid-level / Senior

3. **Issue 3** (Complex):
   - URL: `https://github.com/...`
   - Expected complexity: Senior+

### 5. Do a Full Dry Run (30-60 min)

Follow the timings in [step-by-step/build-guide.md](step-by-step/build-guide.md):

```bash
# Phase 2a (0:05-0:08)
python app.py hello

# Phase 2b (0:08-0:14)  
python app.py hello-stream

# Phase 4 (0:29-0:39) - CLI
python app.py https://github.com/owner/repo/issues/123

# Phase 5 (0:39-0:52) - Web UI
python app.py serve
# Open http://localhost:8000 in browser
# Paste an issue URL and watch stream

# Phase 6 (0:52-0:55) - Write-back
python app.py post https://github.com/owner/repo/issues/123
# Check that comment was posted and label was added
```

## 📊 Your Slide Deck

✅ **Reviewed and approved!** Your 13-slide deck includes:

- Slide 1: Title
- Slide 2: Intro + value proposition
- Slide 3: Agenda (perfectly aligned with your phases)
- Slide 4: What is the SDK (editor vs SDK comparison)
- Slide 5: The Agentic Loop (clear diagram)
- Slide 6-7: Architecture diagram (backend + frontend + API)
- Slide 8+: Resources, learning paths, social

**Status:** Ready to present. Consider noting which slides appear during each phase in your speaker notes.

## 🎥 Quick Reference - What to Demo When

| Time | Phase | Command | What Happens |
|------|-------|---------|---|
| 0:05-0:08 | 2a | `python app.py hello` | Quick SDK response |
| 0:08-0:14 | 2b | `python app.py hello-stream` | Streamed response |
| 0:14-0:29 | 3 | *Live code in editor* | Write 4 tools |
| 0:29-0:39 | 4 | `python app.py <issue_url>` | See tool calls + analysis |
| 0:39-0:52 | 5 | `python app.py serve` + browser | See chat UI streaming |
| 0:52-0:55 | 6a | Scroll to `post_comment()` | Explain write-back logic |
| 0:52-0:55 | 6a | `python app.py post <issue_url>` | Show comment on GitHub |
| 0:55-0:58 | 6b | Scroll to `validate_tool_args()` | Talk through safety hooks |

## 🚀 Ready to Stream!

Once you complete the checklist above, you'll be ready to go live. Your setup is professional and complete:

- ✅ Code is ready (all 6 phases implemented)
- ✅ Slides are ready (13 slides, well-structured)
- ✅ Frontend is ready (pre-built chat UI)
- ✅ Documentation is ready (build-guide, script, slides)
- ✅ Environment automation is ready (devcontainer loads .env)
- ⏳ Token needs to be added (you do this)
- ⏳ Dry run practice (you do this)

**Estimated time to be fully ready:** 20 min (token + test) + 60 min (dry run) = 80 min total prep.

---

**Questions before you go live?** Check [README.md](../README.md) troubleshooting section or [script.md](script.md) for detailed talking points.

Good luck with your livestream! 🎉
