# Livestream Slides

> At most 5 slides. These are for concepts that need a visual, not for code (code lives in the editor).

---

## Slide 1 — Title Slide

**Show at**: 0:00, during intro

| Element | Content |
|---|---|
| Title | **Building an AI Issue Triage Tool with the GitHub Copilot SDK** |
| Subtitle | From empty file to streaming web app in 60 minutes |
| Your name | Renee Noble |
| Logo/branding | GitHub Copilot SDK |
| Optional | QR code or short link to the course repo |

**Agenda** (on the same slide or a quick flash):

1. What is the Copilot SDK?
2. Hello World — Your first SDK call
3. Tools — Giving the model capabilities
4. Building the web UI
5. Safety & writing back to GitHub

---

## Slide 2 — What is the Copilot SDK?

**Show at**: ~0:02, during the SDK primer

This is the key conceptual slide — most of the audience knows Copilot-in-editor but not the SDK.

**Layout suggestion**: Two columns or a before/after visual

| Copilot in your editor | Copilot SDK |
|---|---|
| Built into VS Code, JetBrains, etc. | A Python / JS / C# library you install |
| Suggests code while you type | Your application calls it like any other library |
| You see the results on screen | Your code receives the results and does something with them |
| A tool for developers | A building block for applications |

**What it IS**:
- A library you import in your code, like `requests` or `pandas`
- Your app sends a prompt, gets back text — then your code decides what to do with it
- You can give it tools (functions) that it can call to fetch data or take actions
- It runs inside your app — a web server, a CLI script, a GitHub Action, a Slack bot

**What it is NOT**:
- It's not a chatbot — there's no chat window unless you build one
- It's not sentient — it generates text based on patterns, it doesn't "understand" or "want" things
- It's not magic — it can only use the tools you explicitly give it
- It's not autonomous — your code starts it, your code stops it, your code controls what it can access

**Three building blocks** (icons or simple diagram):

1. **Client** — connects to the Copilot backend (like a database connection)
2. **Session** — a conversation thread where you set the model, tools, and instructions
3. **Tools** — regular functions you write that the model can call during execution

**Key message**: "The SDK lets you embed Copilot into your own applications. You define what it can do. Your code stays in control."

---

## Slide 3 — The Agentic Loop

**Show at**: ~0:14, right before Phase 3 (tools) or ~0:29 before the first live analysis

A simple flow diagram showing how the tool-calling loop works:

```
Prompt → Model generates response → Response includes tool call → Tool executes → Result fed back → Model generates again → ... → Final text response
```

**Visual suggestion**: A loop/cycle diagram with these nodes:

1. 📝 **Prompt sent** — "Analyse this GitHub issue"
2. 🔧 **Model requests tool call** — e.g. `get_github_issue`
3. ⚙️ **Tool executes** — Your code runs, returns data
4. 📖 **Result fed back** — Model receives the tool output
5. ↩️ **Loop** — Model requests more tool calls or produces final output
6. ✅ **Final response** — Structured assessment returned

**Key message**: "We don't script the sequence. The model selects tools based on what information it needs."

---

## Slide 4 — What We Built (Architecture)

**Show at**: ~0:58, during wrap-up (or flash briefly at ~0:39 before Phase 5)

A simple architecture diagram of the finished system:

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

**Key message**: "One file, four layers. The SDK sits in the middle, connecting your UI to the model and your tools."

---

## Slide 5 — Call to Action

**Show at**: 1:00, during wrap-up / leave up during Q&A

| Element | Content |
|---|---|
| **Course** | Link to `github.com/reneenoble/github-copilot-sdk-for-beginners` |
| **This repo** | Link to the stream's repo (if public) |
| **Docs** | Link to Copilot SDK documentation |
| **Try it** | "Clone the repo, set a GITHUB_TOKEN, run `python stream_api.py serve`" |

**Optional extras**:
- QR code for the course link (easy for mobile viewers to scan)
- Social handles for follow-up questions
- "Star the repo" nudge
