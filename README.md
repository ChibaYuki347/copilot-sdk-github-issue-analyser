# 🐛 GitHub Issue Complexity Analyser

> **Livestream Demo**: Building an AI-powered issue triage tool with the GitHub Copilot SDK

An intelligent issue triage tool that analyses GitHub issues in context — fetching issue details, exploring repository structure, reading source code — and produces a structured complexity assessment recommending the appropriate developer skill level for the fix.

Built during a **60-minute livestream** to demonstrate the GitHub Copilot SDK's capabilities.

> **📌 Note**: This is a **clean version** of the project set up for public access. Planning and iteration was done in a [separate repo](https://github.com/reneenoble/gh-copilot-sdk-repo-analyser). The key files to follow along with are the `stream_*` files — particularly [`stream_api.py`](stream_api.py) (the code we build) and [`step-by-step/stream_plan.md`](step-by-step/stream_plan.md) (the build guide).

---

## 📚 Learning Resources

### Getting Started with the Copilot SDK

| Resource | Description |
|----------|-------------|
| 📖 [Official SDK Documentation](https://github.com/github/copilot-sdk) | GitHub Copilot SDK repo and docs |
| 🎓 [Copilot SDK for Beginners Course](https://github.com/reneenoble/gh-copilot-sdk-repo-analyser) | *Draft* — A hands-on course teaching you to build AI agents with the SDK |
| 🛠️ [Copilot CLI Installation](https://docs.github.com/en/copilot/github-copilot-in-the-cli) | Set up the GitHub Copilot CLI (required for the SDK) |

### What is the Copilot SDK?

| Copilot in your editor | Copilot SDK |
|------------------------|-------------|
| Built into VS Code, JetBrains, etc. | A Python / JS / C# library you install |
| Suggests code while you type | Your application calls it like any other library |
| You see the results on screen | Your code receives the results and decides what to do |
| A tool for developers | A building block for applications |

**The SDK lets you embed Copilot into your own applications.** You define what it can do. Your code stays in control.

**Three building blocks:**
1. **Client** — connects to the Copilot backend (like a database connection)
2. **Session** — a conversation thread where you set the model, tools, and instructions
3. **Tools** — regular functions you write that the model can call during execution

---

## ✨ Features

| Feature | CLI | Web App |
|---------|-----|---------|
| Issue analysis by URL or owner/repo/number | ✅ | ✅ |
| Real-time streaming output | ✅ (terminal) | ✅ (SSE chat UI) |
| Tool call visibility (which files/APIs are being queried) | ✅ | ✅ |
| Structured Markdown assessment | ✅ | ✅ (rendered) |
| REST API for integration | — | ✅ |
| Post analysis back to GitHub | ✅ | ✅ |

### Copilot SDK Concepts Demonstrated

- **`CopilotClient`** — session creation and lifecycle management
- **`@define_tool`** — custom tool definitions with Pydantic parameter schemas
- **Agentic tool calling** — Copilot autonomously invokes your Python functions to gather context
- **Streaming event handling** — real-time processing of `assistant.message`, `tool.call`, and `session.idle` events
- **Multi-turn tool loops** — the agent makes multiple rounds of tool calls before producing its final assessment

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────┐
│  Browser (pre-built frontend)            │
│  EventSource → renders chat bubbles      │
└────────────────┬─────────────────────────┘
                 │ SSE (Server-Sent Events)
                 ▼
┌──────────────────────────────────────────┐
│  FastAPI Server (stream_api.py)          │
│  /analyse/stream + /post-analysis        │
│  async queue bridges SDK → SSE           │
└────────────────┬─────────────────────────┘
                 │ Copilot SDK
                 ▼
┌──────────────────────────────────────────┐
│  Copilot Backend (gpt-4.1)              │
│  Generates responses + tool calls        │
└────────────────┬─────────────────────────┘
                 │ Tool calls
                 ▼
┌──────────────────────────────────────────┐
│  GitHub REST API                         │
│  Issues · Contents · Code Search         │
└──────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **GitHub Copilot CLI** installed and authenticated ([quick guide](https://docs.github.com/en/copilot/github-copilot-in-the-cli))
- **GitHub Token** (optional but recommended) — set `GITHUB_TOKEN` or `GH_TOKEN` for higher API rate limits

### Setup

```bash
# Clone the repository
git clone https://github.com/reneenoble/copilot-sdk-github-issue-analyser-.git
cd copilot-sdk-github-issue-analyser-

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -e .

# (Optional) Set GitHub token for higher rate limits
export GITHUB_TOKEN=ghp_your_token_here
```

### Usage

```bash
# Test the SDK (Phase 2a: simplest call)
python stream_api.py hello

# Test with streaming (Phase 2b)
python stream_api.py hello-stream

# Analyse an issue by URL
python stream_api.py https://github.com/microsoft/vscode/issues/12345

# Analyse by owner/repo/number
python stream_api.py microsoft vscode 12345

# Start the web UI
python stream_api.py serve

# Analyse and post results back to GitHub
python stream_api.py post https://github.com/your-org/your-repo/issues/123
```

---

## 📂 Project Structure

```
copilot-sdk-github-issue-analyser/
├── stream_api.py           # ⭐ Main file built during livestream (CLI + API + tools)
├── src/
│   ├── issue_analyser.py   # Standalone CLI version (reference)
│   ├── hello_world.py      # Minimal SDK example
│   └── static/             # Pre-built web frontend (HTML/CSS/JS)
├── step-by-step/           # ⭐ Livestream materials
│   ├── stream_plan.md      # ⭐ Phase-by-phase build plan (follow this!)
│   ├── stream-slides.md    # Slide deck content
│   └── script_stream.md    # Full script with code snippets
├── docs/
│   ├── RAI.md              # Responsible AI notes
│   └── architecture.md     # Architecture details
├── pyproject.toml          # Python dependencies
├── AGENTS.md               # Agent instructions for Copilot
└── README.md               # This file
```

> **💡 Key files**: The `stream_*` files are the primary learning resources. `stream_api.py` is the code built during the stream, and `step-by-step/stream_plan.md` is the phase-by-phase guide.

---

## 🎬 Livestream Build Plan

The tool was built in **6 phases** during a 60-minute livestream:

| Phase | Time | What We Built |
|-------|------|---------------|
| 1 | 0:00–0:05 | Imports + intro |
| 2a | 0:05–0:08 | Hello World with `send_and_wait` |
| 2b | 0:08–0:14 | Streaming with events |
| 3 | 0:14–0:29 | Custom tools (`@define_tool`) |
| 4 | 0:29–0:39 | System prompt + CLI analyser |
| 5 | 0:39–0:52 | FastAPI + Server-Sent Events |
| 6a | 0:52–0:55 | Write back to GitHub |
| 6b | 0:55–0:58 | Safety hooks (talk only) |

**Wrap-up**: 0:58–1:00 · **Q&A**: 1:00–1:15

See [`step-by-step/stream_plan.md`](step-by-step/stream_plan.md) for the complete phase-by-phase guide with code.

---

## 🔗 Links

- 📖 **[Copilot SDK Documentation](https://github.com/github/copilot-sdk)**
- 🎓 **[Copilot SDK for Beginners Course](https://github.com/reneenoble/gh-copilot-sdk-repo-analyser)** *(Draft)*
- 🛠️ **[Copilot CLI Setup Guide](https://docs.github.com/en/copilot/github-copilot-in-the-cli)**
- 📋 **[Copilot Plans & Pricing](https://github.com/features/copilot/plans)** (includes free tier!)

---

## ⚖️ Responsible AI Notes

See [docs/RAI.md](docs/RAI.md) for full details. Key points:

- **Not a replacement for human judgement** — the assessment is a starting point for triage discussions
- **Skill level labels are contextual** — "Junior" and "Senior" refer to familiarity with the specific codebase
- **No personal data processing** — only reads public GitHub issue data and repository content
- **Full transparency** — every tool call is visible so users can see exactly what the agent examined

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.
