# 🎬 Presenter Resources

All materials needed to present the GitHub Issue Complexity Analyser livestream are here.

## 📋 Quick Navigation

### For Immediate Prep
- **[`LIVESTREAM_PREP.md`](LIVESTREAM_PREP.md)** — **START HERE** (20 min)
  - ✅ What's been set up for you
  - ⏳ What you still need to do (token + test)
  - 📊 Checklist with timing estimates

### For Running the Stream
- **[`script.md`](script.md)** — 60-minute talking points
  - What to say at each phase
  - Demo commands and expected output
  - Timing cues (0:00–0:05, etc.)
  - Talking points for complex concepts

- **[`AI_Genius_Copilot_SDK_Ep3_EN.pdf`](AI_Genius_Copilot_SDK_Ep3_EN.pdf)** — Presentation deck (PDF)
  - Title, agenda, architecture, and resources
  - Use during intro, architecture walkthrough, and wrap-up

### For Pre-Stream Testing
- **[`pre-stream-check.sh`](pre-stream-check.sh)** — Automated verification
  ```bash
  bash pre-stream-check.sh
  ```
  Checks:
  - ✅ Python installation
  - ✅ All dependencies (Copilot SDK, FastAPI, Pydantic, httpx)
  - ✅ GitHub token is set
  - ✅ Copilot CLI works
  - ✅ Phase 2a and 2b execute without errors

---

## 🚀 Presenter Workflow

### Week Before
1. Read [`LIVESTREAM_PREP.md`](LIVESTREAM_PREP.md) fully
2. Review [`script.md`](script.md) talking points
3. Prepare 2-3 GitHub issue URLs to demo (varying complexity)

### Day Before
1. Create fresh GitHub token (7-day expiration)
2. Add token to `.env` in repo root
3. Run `bash presenter-resources/pre-stream-check.sh`
4. Test all 6 phases manually:
   ```bash
   python app.py hello               # Phase 2a
   python app.py hello-stream        # Phase 2b
   python app.py serve               # Phase 5 (web UI)
   ```

### Day Of (60 min before stream)
1. Run pre-stream check again
2. Arrange screen layout (VS Code left, terminal bottom, browser right)
3. Have your 3 test issues ready in browser tabs
4. Open `script.md` in a second editor/monitor as speaker notes
5. Have `AI_Genius_Copilot_SDK_Ep3_EN.pdf` open and ready

### During Stream
1. Follow timing in `script.md` (each phase has a time code)
2. Pause at key moments to explain concepts
3. Run demos exactly as written in the script
4. If something breaks, pivot to explanation slides or Q&A

---

## 📂 File Details

| File | Purpose | Audience |
|------|---------|----------|
| `LIVESTREAM_PREP.md` | Setup checklist & timeline | Presenter (before stream) |
| `pre-stream-check.sh` | Automated test script | Presenter (before stream) |
| `script.md` | 60-min talking points + demos | Presenter (during stream) |
| `AI_Genius_Copilot_SDK_Ep3_EN.pdf` | Presentation deck (PDF) | Presenter + viewers (during stream) |

---

## ❓ FAQ

**Q: I'm not sure if everything is ready. What do I run?**  
A: `bash pre-stream-check.sh` — it will tell you what's missing.

**Q: Where do I put my GitHub token?**  
A: In `.env` file in the repo root (one level up from this folder). See `LIVESTREAM_PREP.md` for steps.

**Q: How long is the livestream?**  
A: 60 minutes total: ~5 min intro + 55 min build + 15 min Q&A = 75 min (tight, pace yourself).

**Q: Can I edit the script or deck?**  
A: Absolutely! `script.md` and `AI_Genius_Copilot_SDK_Ep3_EN.pdf` are yours to customize. The timing is approximate—adjust as needed.

**Q: What if Phase 2a or 2b fail?**  
A: Run `python app.py hello` outside the check script to see the full error. Usually means missing token or SDK issue. The pre-stream check will catch this.

---

## 🎯 Success Criteria

Before you go live, confirm:
- ✅ `bash pre-stream-check.sh` passes completely
- ✅ You can run `python app.py hello` and get an SDK response
- ✅ You can run `python app.py serve` and open http://localhost:8000
- ✅ Your 3 test GitHub issues are bookmarked and tested
- ✅ VS Code, terminal, and browser tabs are arranged
- ✅ You've read the timing in `script.md` (0:00–1:00)

**You're ready to stream!** 🚀
