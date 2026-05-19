# 🐛 GitHub Issue Complexity Analyser

> 🌏 **Language / 言語**: **English (original)** · [日本語版 (Japanese version)](README.ja.md)
>
> Original workshop by **Renee Noble** ([reneenoble/copilot-sdk-github-issue-analyser](https://github.com/reneenoble/copilot-sdk-github-issue-analyser)).
> Japanese version maintained by **@ChibaYuki347** on the [`ja`](https://github.com/ChibaYuki347/copilot-sdk-github-issue-analyser/tree/ja) branch of [his fork](https://github.com/ChibaYuki347/copilot-sdk-github-issue-analyser). MIT License.

> **Livestream Demo**: Building an AI-powered issue triage tool with the GitHub Copilot SDK

An intelligent issue triage tool that analyses GitHub issues in context - fetching issue details, exploring repository structure, reading source code - and produces a structured complexity assessment recommending the appropriate developer skill level for the fix.

Built during a **60-minute livestream** to demonstrate the GitHub Copilot SDK's capabilities.

> **📌 Note**: This is a **clean version** of the project set up for public access. Planning and iteration was done in a [separate repo](https://github.com/reneenoble/gh-copilot-sdk-repo-analyser). The key files to follow along with are [`app.py`](app.py) (the code we build) and [`step-by-step/build-guide.md`](step-by-step/build-guide.md) (the phase-by-phase guide).

---

## 📚 Learning Resources

### Getting Started with the Copilot SDK

| Resource | Description |
|----------|-------------|
| 📖 [Official SDK Documentation](https://github.com/github/copilot-sdk) | GitHub Copilot SDK repo and docs |
| 🎓 [Copilot SDK for Beginners Course](https://github.com/reneenoble/gh-copilot-sdk-repo-analyser) | *Draft* - A hands-on course teaching you to build AI agents with the SDK |
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
1. **Client** - connects to the Copilot backend (like a database connection)
2. **Session** - a conversation thread where you set the model, tools, and instructions
3. **Tools** - regular functions you write that the model can call during execution

---

## ✨ Features

| Feature | CLI | Web App |
|---------|-----|---------|
| Issue analysis by URL or owner/repo/number | ✅ | ✅ |
| Real-time streaming output | ✅ (terminal) | ✅ (SSE chat UI) |
| Tool call visibility (which files/APIs are being queried) | ✅ | ✅ |
| Structured Markdown assessment | ✅ | ✅ (rendered) |
| REST API for integration | - | ✅ |
| Post analysis back to GitHub | ✅ | ✅ |

### Copilot SDK Concepts Demonstrated

- **`CopilotClient`** - session creation and lifecycle management
- **`@define_tool`** - custom tool definitions with Pydantic parameter schemas
- **Agentic tool calling** - Copilot autonomously invokes your Python functions to gather context
- **Streaming event handling** - real-time processing of `assistant.message`, `tool.call`, and `session.idle` events
- **Multi-turn tool loops** - the agent makes multiple rounds of tool calls before producing its final assessment

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
│  FastAPI Server (app.py)          │
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

### Option 1: GitHub Codespaces (recommended for the stream)

The easiest way to get started — everything is pre-configured in the devcontainer.

1. Click **Code** → **Codespaces** → **Create codespace on main**
2. When prompted, enter your **GitHub personal access token** (the Codespace will ask for it automatically)
3. Wait for the setup to finish — Python, dependencies, and the Copilot SDK are all installed for you
4. You're ready to go!

### Option 2: Local Dev Container

For a Codespaces-like experience locally with full isolation:

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Install the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension in VS Code
3. Open this folder in VS Code → click "Reopen in Container" (bottom-left)
4. VS Code builds the container from `docker-compose.yml` and automatically:
   - Loads your `.env` file with `GITHUB_TOKEN`
   - Installs Python and dependencies
   - Sets up the GitHub CLI extension
5. You're ready to go!

<details>
<summary><b>New to Dev Containers?</b> Click to expand.</summary>

Dev Containers let you develop inside a Docker container as if it were your local machine. All your tools, dependencies, and environment variables are isolated and reproducible.

- **[Dev Containers Documentation](https://containers.dev/)** — Official spec and guides
- **[VS Code Remote Development](https://code.visualstudio.com/docs/remote/remote-overview)** — How to use with VS Code
- **Benefits**: Consistent environments across team, no "works on my machine" problems, easy onboarding

For this project, you don't need to understand Docker internals—just think of it as "VS Code in a sandboxed environment that has everything pre-installed."

</details>

### Option 3: Local Python (No Container)

For a quick local setup without containerization:

Prerequisites:
- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)** (Python package manager)
- **GitHub Token** — needed for API access and Copilot SDK auth

#### Setup

```bash
# Clone the repository
git clone https://github.com/reneenoble/copilot-sdk-github-issue-analyser-.git
cd copilot-sdk-github-issue-analyser-

# Create .env file with your GitHub token
cp .env.example .env
# Then edit .env and add your token:
#   GITHUB_TOKEN=ghp_your_token_here

# Install dependencies
uv sync

# Alternatively, export the token in your shell
export GITHUB_TOKEN=ghp_your_token_here
```

### Getting a GitHub Token

All three options require a GitHub personal access token. Create one with the correct permissions:

1. Go to **github.com** → your profile picture (top right) → **Settings**
2. Scroll down left sidebar → **Developer settings** → **Personal access tokens** → **Fine-grained tokens**
3. Click **Generate new token**
   - Name: `copilot-sdk-stream` (or similar)
   - Expiration: 7 days (sufficient for a demo)
   - Repository access: **All repositories**
   - Permissions:
     - **Issues**: Read and Write
     - **Contents**: Read
4. Click **Generate token** and copy it
5. Add to `.env`: `GITHUB_TOKEN=ghp_...` (or export as shown above)

### Usage

```bash
# Test the SDK (Phase 2a: simplest call)
python app.py hello

# Test with streaming (Phase 2b)
python app.py hello-stream

# Analyse an issue by URL
python app.py https://github.com/microsoft/vscode/issues/12345

# Analyse by owner/repo/number
python app.py microsoft vscode 12345

# Start the web UI
python app.py serve

# Analyse and post results back to GitHub
python app.py post https://github.com/your-org/your-repo/issues/123
```

---

## 📂 Project Structure

```
copilot-sdk-github-issue-analyser/
├── app.py                  # ⭐ Main file built during livestream (CLI + API + tools)
├── src/
│   ├── hello_world.py      # Minimal SDK example (start here!)
│   └── static/             # Pre-built web frontend (HTML/CSS/JS)
├── step-by-step/
│   └── build-guide.md      # ⭐ Phase-by-phase build plan (follow this!)
├── presenter-resources/    # ⭐ Presenter-only materials
│   ├── LIVESTREAM_PREP.md
│   ├── pre-stream-check.sh
│   ├── script.md
│   └── AI_Genius_Copilot_SDK_Ep3_EN.pdf
├── docs/
│   ├── RAI.md              # Responsible AI notes
│   └── architecture.png    # Architecture diagram
├── pyproject.toml          # Python dependencies
├── AGENTS.md               # Agent instructions for Copilot
└── README.md               # This file
```

> **💡 Key files**: `app.py` is the code built during the livestream, and `step-by-step/build-guide.md` is the phase-by-phase guide.

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

See [`step-by-step/build-guide.md`](step-by-step/build-guide.md) for the complete phase-by-phase guide with code.

---

## 🎥 Livestream Presenter Setup

If you're presenting this livestream, **refer to the [`presenter-resources/`](presenter-resources/) folder** for all presenter materials, including:
- **[`LIVESTREAM_PREP.md`](presenter-resources/LIVESTREAM_PREP.md)** — Complete setup checklist and timeline
- **[`pre-stream-check.sh`](presenter-resources/pre-stream-check.sh)** — Automated environment verification script
- **[`AI_Genius_Copilot_SDK_Ep3_EN.pdf`](presenter-resources/AI_Genius_Copilot_SDK_Ep3_EN.pdf)** — Presentation deck (PDF)
- **[`script.md`](presenter-resources/script.md)** — Detailed 60-minute talking points and demo script

### Quick Start: Before You Go Live (30 min prep)

```bash
# 1. Create a fresh GitHub token (expires in 7 days)
#    Go to: https://github.com/settings/tokens?type=beta
#    Permissions: Issues (read/write), Contents (read)

# 2. Add token to .env file
cp .env.example .env
# Edit .env and paste your token

# 3. Run pre-stream check
bash presenter-resources/pre-stream-check.sh

# 4. Full setup and timeline: see presenter-resources/LIVESTREAM_PREP.md
```

### Screen Layout for Streaming

Arrange your screen so viewers can see:
1. **VS Code** (editor) — left side with `app.py` open
2. **Terminal** (output) — bottom with live execution
3. **Browser** (optional) — right side with `http://localhost:8000` for Phase 5 demo
4. **Slide deck (PDF)** — `presenter-resources/AI_Genius_Copilot_SDK_Ep3_EN.pdf` (off-screen or second monitor)

### Key Demos to Prepare

| Phase | Demo | Expected Output |
|-------|------|---|
| 2a | `python app.py hello` | 2-sentence answer about the SDK |
| 2b | `python app.py hello-stream` | Same answer, streamed token-by-token |
| 4 | `python app.py <issue_url>` | Full analysis with tool calls printed |
| 5 | Open `http://localhost:8000` → paste issue URL → watch stream in browser | Chat UI with animated tool calls |
| 6 | Check issue on GitHub | New comment posted + difficulty label added |

### Troubleshooting

- **"GITHUB_TOKEN not found"** → Check `.env` file or `export GITHUB_TOKEN=...`
- **"Rate limit exceeded"** → Your token isn't being read; verify `GITHUB_TOKEN` is set
- **"Model not available"** → Verify you have Copilot access; check with `copilot --version`
- **Browser won't connect to SSE** → Try `http://127.0.0.1:8000` instead of `localhost`

---

## 🔗 Links

- 📖 **[Copilot SDK Documentation](https://github.com/github/copilot-sdk)**
- 🎓 **[Copilot SDK for Beginners Course](https://github.com/reneenoble/gh-copilot-sdk-repo-analyser)** *(Draft)*
- 🛠️ **[Copilot CLI Setup Guide](https://docs.github.com/en/copilot/github-copilot-in-the-cli)**
- 📋 **[Copilot Plans & Pricing](https://github.com/features/copilot/plans)** (includes free tier!)

---

## ⚖️ Responsible AI Notes

See [docs/RAI.md](docs/RAI.md) for full details. Key points:

- **Not a replacement for human judgement** - the assessment is a starting point for triage discussions
- **Skill level labels are contextual** - "Junior" and "Senior" refer to familiarity with the specific codebase
- **No personal data processing** - only reads public GitHub issue data and repository content
- **Full transparency** - every tool call is visible so users can see exactly what the agent examined

---

## 📄 License

MIT - see [LICENSE](LICENSE) for details.
