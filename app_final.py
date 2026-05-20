"""
app_final.py — GitHub Issue Complexity Analyser

Built step-by-step during the livestream. Frontend is pre-built in src/static/.

Usage:
  python app_final.py hello                          # Phase 2a: Simplest SDK call
  python app_final.py hello-stream                   # Phase 2b: Streaming events
  python app_final.py <github_issue_url>             # Phase 4: CLI analysis
  python app_final.py <owner> <repo> <issue_number>  # Phase 4: CLI analysis
  python app_final.py serve                          # Phase 5: Start web UI (post via the UI button)
"""

# =================================================================
# PHASE 1 — Imports
# =================================================================

import asyncio
import base64
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from copilot import CopilotClient, define_tool
from copilot.session import PermissionHandler

# Load environment variables from .env file (GITHUB_TOKEN, etc.)
load_dotenv()

# Optional: terminal usage logger. No-op unless SHOW_USAGE=1 is set.
import extras_usage  # noqa: F401


# =================================================================
# PHASE 2a — Hello World with send_and_wait (simplest possible)
#
# Three concepts: Client → Session → Response
# send_and_wait() blocks until the full response is ready.
# =================================================================

async def hello_world():
    """Simplest example: send a prompt, get the full response back."""
    client = CopilotClient()
    await client.start()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    session = await client.create_session(
        model="gpt-4.1",
        on_permission_request=PermissionHandler.approve_all,
        github_token=token,
    )
    response = await session.send_and_wait("What is the GitHub Copilot SDK in 2 sentences?")
    if response and getattr(response, "data", None) and hasattr(response.data, "content"):
        print(response.data.content)

    await session.disconnect()
    await client.stop()

# Command to run this phase: python app_final.py hello


# =================================================================
# PHASE 2b — Streaming with Events
#
# Same thing, but now we see tokens arrive in real-time.
# This is the pattern we'll use for the rest of the stream.
# Event types: assistant.message, tool.call, session.idle
# =================================================================

async def hello_world_streaming():
    """Stream the response token by token using events."""
    client = CopilotClient()
    await client.start()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    session = await client.create_session(
        model="gpt-4.1",
        on_permission_request=PermissionHandler.approve_all,
        github_token=token,
    )

    # The SDK emits events as the session runs. We listen for:
    done = asyncio.Event()

    def on_event(event):
        """
            Handle events emitted by the session. We look for:
            - assistant.message: new tokens from the assistant (print them)
            - session.idle: the session has finished processing (set the done event)
        """ 
        if event.type.value == "assistant.message":
            # Print tokens as they arrive, without a newline, and flush to ensure real-time display.
            print(event.data.content, end="", flush=True)
        elif event.type.value == "session.idle":
            done.set()

    # Register the event handler before sending the message
    session.on(on_event)
    await session.send("What is the GitHub Copilot SDK in 2 sentences?")
    # Wait until the session is idle (response is complete) before proceeding.
    await done.wait()

    print()
    await session.disconnect()
    await client.stop()

# Command to run this phase: python app_final.py hello-stream


# =================================================================
# PHASE 3 — Custom Tools with @define_tool
#
# Tools let the agent interact with the outside world.
# You define a function + Pydantic params, and the agent decides
# when and how to call it. That's the "agentic" part.
# =================================================================

def github_api(endpoint: str) -> dict:
    """Call the GitHub REST API (shared helper for all tools)."""
    import httpx

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "copilot-livestream",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    with httpx.Client() as http:
        resp = http.get(f"https://api.github.com{endpoint}", headers=headers)
        resp.raise_for_status()
        return resp.json()


# --- Tool 1: Fetch issue details ---

class GetIssueParams(BaseModel):
    owner: str = Field(description="Repository owner (e.g. 'microsoft')")
    repo: str = Field(description="Repository name (e.g. 'vscode')")
    issue_number: int = Field(description="Issue number")


@define_tool(description="Fetch a GitHub issue including title, body, labels, and comments")
async def get_github_issue(params: GetIssueParams) -> str:
    try:
        issue = github_api(
            f"/repos/{params.owner}/{params.repo}/issues/{params.issue_number}"
        )
        comments = github_api(
            f"/repos/{params.owner}/{params.repo}/issues/{params.issue_number}/comments"
        )
        return str({
            "title": issue["title"],
            "body": issue.get("body", "No description"),
            "labels": [l["name"] for l in issue.get("labels", [])],
            "user": issue["user"]["login"],
            "comments": [
                {"user": c["user"]["login"], "body": c["body"][:500]}
                for c in comments[:5]
            ],
        })
    except Exception as e:
        return f"Error fetching issue: {e}"


# --- Tool 2: Explore repo structure ---

class RepoStructureParams(BaseModel):
    owner: str = Field(description="Repository owner")
    repo: str = Field(description="Repository name")
    path: str = Field(default="", description="Directory path (empty for root)")


@define_tool(description="List the directory contents of a GitHub repository")
async def get_repo_structure(params: RepoStructureParams) -> str:
    try:
        items = github_api(
            f"/repos/{params.owner}/{params.repo}/contents/{params.path}"
        )
        if isinstance(items, list):
            return "\n".join(
                f"{'📁' if i['type'] == 'dir' else '📄'} {i['path']}"
                for i in items[:50]
            )
        return f"File: {items['path']}"
    except Exception as e:
        return f"Error: {e}"


# --- Tool 3: Search code ---

class SearchCodeParams(BaseModel):
    owner: str = Field(description="Repository owner")
    repo: str = Field(description="Repository name")
    query: str = Field(description="Search keywords")


@define_tool(description="Search for code in a GitHub repository")
async def search_code_in_repo(params: SearchCodeParams) -> str:
    try:
        results = github_api(
            f"/search/code?q={params.query}+repo:{params.owner}/{params.repo}&per_page=10"
        )
        files = [
            {"path": i["path"], "name": i["name"]}
            for i in results.get("items", [])[:10]
        ]
        return str(files) if files else "No matching code found"
    except Exception as e:
        return f"Error: {e}"


# --- Tool 4: Read file contents ---

class FileContentParams(BaseModel):
    owner: str = Field(description="Repository owner")
    repo: str = Field(description="Repository name")
    path: str = Field(description="File path within the repository")


@define_tool(description="Fetch and read a specific file from a GitHub repository")
async def get_file_content(params: FileContentParams) -> str:
    try:
        data = github_api(
            f"/repos/{params.owner}/{params.repo}/contents/{params.path}"
        )
        if data.get("encoding") == "base64":
            text = base64.b64decode(data["content"]).decode("utf-8")
            if len(text) > 5000:
                return text[:5000] + "\n...[truncated]"
            return text
        return data.get("content", "Unable to decode")
    except Exception as e:
        return f"Error: {e}"


# =================================================================
# PHASE 4 — System Prompt + CLI Analyser
#
# The system prompt shapes the agent's behaviour. The tools list
# tells the SDK what the agent CAN do. The agent autonomously
# decides WHICH tools to call and in what order.
# =================================================================

# List the tools we just made
TOOLS = [get_github_issue, get_repo_structure, search_code_in_repo, get_file_content]

# Create the system prompt that guides the agent's behaviour. 
# This is where you inject the "personality" and instructions for the agent. 
# You can include formatting instructions, reasoning steps, and any constraints or guidelines
#
# =================================================================
# Locale support — minimal en/ja switching (日本語版独自の追加)
# Set LANG=ja or APP_LANG=ja to render system prompt + CLI in Japanese.
# 既定は en で、upstream の挙動と等価です。
# =================================================================

LANG = (os.environ.get("APP_LANG") or os.environ.get("LANG") or "en")[:2].lower()
if LANG not in ("en", "ja"):
    LANG = "en"

SYSTEM_PROMPT_EN = """You are a senior engineering manager triaging GitHub issues.

When given an issue to analyse, you will:
1. Fetch the issue details using the get_github_issue tool
2. Explore the repository structure to understand the codebase
3. Search for and read relevant source files
4. Provide a structured complexity assessment

Format your response as:
## Issue Summary
## Complexity Assessment
- **Recommended Skill Level**: Junior / Mid-level / Senior / Senior+
- **Confidence**: High / Medium / Low
## Reasoning
## Files Likely Involved
## Suggested Approach
## Mentorship Notes
Include what a less experienced developer would need to learn to tackle this issue."""

SYSTEM_PROMPT_JA = """あなたは GitHub Issue をトリアージするシニアエンジニアリングマネージャーです。

解析する Issue が与えられたら、次を行います:
1. `get_github_issue` ツールを使って Issue の詳細を取得します
2. コードベースを理解するために、リポジトリ構造を探索します
3. 関連するソースファイルを検索して読みます
4. 構造化された複雑さ評価を提供します

回答は次の形式にしてください:
## Issue の要約
## 複雑さ評価
- **推奨スキルレベル**: ジュニア / ミドル / シニア / シニア+
- **確信度**: 高 / 中 / 低
## 理由
## 関係する可能性が高いファイル
## 提案する進め方
## メンタリングのヒント
この Issue に取り組むために、経験の浅い開発者が何を学ぶ必要があるかも含めてください。
スキルレベルのラベルは年次ではなくコードベースへの習熟度を指します。"""

SYSTEM_PROMPT = SYSTEM_PROMPT_JA if LANG == "ja" else SYSTEM_PROMPT_EN

MESSAGES = {
    "en": {
        "analysing": "🔍 Analysing issue #{issue_number} in {owner}/{repo}...",
        "tool_running": "🔧 {tool}...",
        "comment_posted": "💬 Comment posted to {owner}/{repo}#{issue_number}",
        "labels_added": "🏷️  Labels added: {labels}",
        "analyse_prompt": "Please analyse GitHub issue #{issue_number} in {owner}/{repo}.",
        "cli_title": "🐛 GitHub Issue Complexity Analyser — Livestream Build",
        "cli_arg_error": "Error: Invalid arguments. Run without args for usage.",
    },
    "ja": {
        "analysing": "🔍 {owner}/{repo} の Issue #{issue_number} を解析しています...",
        "tool_running": "🔧 {tool} を実行しています...",
        "comment_posted": "💬 {owner}/{repo}#{issue_number} にコメントを投稿しました",
        "labels_added": "🏷️  ラベルを追加しました: {labels}",
        "analyse_prompt": "{owner}/{repo} の GitHub Issue #{issue_number} を解析してください。",
        "cli_title": "🐛 GitHub Issue Complexity Analyser — ライブ配信ビルド",
        "cli_arg_error": "エラー: 引数が不正です。使い方を表示するには引数なしで実行してください。",
    },
}


def msg(key: str, **fmt) -> str:
    """Look up a localized message and format it. Falls back to English."""
    template = MESSAGES.get(LANG, MESSAGES["en"]).get(key) or MESSAGES["en"][key]
    return template.format(**fmt) if fmt else template


# This function is much like Phase 2b, but now the agent can 
# call tools, has a system prompt, and has logic to handle output for different tool calls
async def analyse_cli(owner: str, repo: str, issue_number: int):
    """Run analysis in the terminal with streaming output."""
    print(f"\n{msg('analysing', owner=owner, repo=repo, issue_number=issue_number)}\n")

    client = CopilotClient()
    await client.start()

    # Set up the session but give it tools this time
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    session = await client.create_session(
        model="gpt-4.1",
        tools=TOOLS,
        on_permission_request=PermissionHandler.approve_all,
        github_token=token,
    )

    done = asyncio.Event()


    # Set up handling of the different event types. 
    # assistant.message is the main response stream, 
    # but we also watch for tool calls to display them and session idle to finish up
    def on_event(event):
        name = event.type.value if hasattr(event.type, "value") else str(event.type)
        if name == "assistant.message":
            print(event.data.content, end="", flush=True)
        elif name in ("tool.call", "tool.execution_start"):
            tool = getattr(event.data, "name", None) or getattr(event.data, "tool_name", "")
            print(f"\n{msg('tool_running', tool=tool)}", flush=True)
        elif name == "session.idle":
            done.set()

    session.on(on_event)
    # Send a message, now using your system prompt and the specific issue to analyse. 
    await session.send(
        f"{SYSTEM_PROMPT}\n\n{msg('analyse_prompt', owner=owner, repo=repo, issue_number=issue_number)}"
    )
    await done.wait()

    print("\n")
    await session.disconnect()
    await client.stop()

# Command to run this phase: python app_final.py <owner> <repo> <issue_number>
# Example: python app_final.py microsoft vscode 12345


# =================================================================
# PHASE 5 — FastAPI + Server-Sent Events
#
# SSE lets us stream the agent's thinking to the browser in
# real-time. Each tool call and message chunk becomes an event
# the pre-built frontend renders as chat bubbles.
# =================================================================

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse

app = FastAPI(title="GitHub Issue Complexity Analyser")

# Serve the pre-built frontend
static_dir = Path(__file__).parent / "src" / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    return FileResponse(static_dir / "index.html")


@app.get("/health")
async def health():
    return {"status": "healthy"}


# There is a helper function _parse_args we wrote for you (at the bottom of the file) that you can use to 
# handle the various formats tool arguments might come in (dict, JSON string, Pydantic model). 




async def stream_analysis(owner: str, repo: str, issue_number: int):
    """Async generator that yields Server-Sent Events for the frontend."""
    
    # Same session setup as above
    client = CopilotClient()
    await client.start()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    session = await client.create_session(
        model="gpt-4.1",
        tools=TOOLS,
        on_permission_request=PermissionHandler.approve_all,
        github_token=token,
    )

    queue = asyncio.Queue()
    
    # Set up event handling to push messages and tool calls into the queue for streaming to the frontend.
    def on_event(event):
        name = event.type.value if hasattr(event.type, "value") else str(event.type)

        if name == "assistant.message":
            content = getattr(event.data, "content", "")
            if content and content.strip():
                queue.put_nowait(("message", content))

        elif name == "tool.execution_start":
            # Emitted once per tool invocation, before the tool runs
            tool_name = getattr(event.data, "tool_name", None)
            args = _parse_args(getattr(event.data, "arguments", None))
            if tool_name:
                queue.put_nowait(("tool_call", {"name": tool_name, "args": args}))

        elif name == "session.idle":
            queue.put_nowait(("done", None))

    # Send off the same message as before, but now the GitHub Issue info has come 
    # from query parameters collected when the analyse/stream endpoint calls this function.
    session.on(on_event)
    await session.send(
        f"{SYSTEM_PROMPT}\n\n{msg('analyse_prompt', owner=owner, repo=repo, issue_number=issue_number)}"
    )

    # Stream events to the frontend as they come in. The frontend will render them as chat bubbles and tool call notifications.
    while True:
        event_type, data = await queue.get()
        if event_type == "message":
            yield f"event: message\ndata: {json.dumps({'content': data})}\n\n"
        elif event_type == "tool_call":
            yield f"event: tool_call\ndata: {json.dumps(data)}\n\n"
        elif event_type == "done":
            yield f"event: done\ndata: {json.dumps({'status': 'complete'})}\n\n"
            break

    await session.disconnect()
    await client.stop()


@app.get("/analyse/stream")
async def analyse_stream(owner: str, repo: str, issue_number: int):
    """Stream analysis results to the frontend via SSE."""
    return StreamingResponse(
        stream_analysis(owner, repo, issue_number),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


# Command to run this phase: python app_final.py serve
# Then open http://localhost:8000 in the browser and enter the repo and issue number

# =================================================================
# PHASE 6a — Write Back to GitHub (human-triggered via UI button)
#
# After the analysis streams in, the user reviews it and clicks
# "Post to GitHub". This endpoint posts the comment and adds
# a difficulty label. Human-in-the-loop = safer.
#
# Requires GITHUB_TOKEN with write permissions:
#   - Classic tokens: repo scope
#   - Fine-grained tokens: Issues → Read and Write
# =================================================================

SKILL_LABELS = {
    "junior": ["good first issue", "difficulty: easy"],
    "mid-level": ["difficulty: medium"],
    "senior": ["difficulty: hard"],
    "senior+": ["difficulty: expert"],
}


async def post_comment(owner: str, repo: str, issue_number: int, body: str):
    """Post a comment on a GitHub issue."""
    import httpx

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    async with httpx.AsyncClient() as http:
        resp = await http.post(
            f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
            json={"body": body},
        )
        resp.raise_for_status()
    print(msg('comment_posted', owner=owner, repo=repo, issue_number=issue_number))


async def add_labels(owner: str, repo: str, issue_number: int, labels: list[str]):
    """Add labels to a GitHub issue."""
    import httpx

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    async with httpx.AsyncClient() as http:
        resp = await http.post(
            f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/labels",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
            json={"labels": labels},
        )
        resp.raise_for_status()
    print(msg('labels_added', labels=", ".join(labels)))


class PostAnalysisRequest(BaseModel):
    owner: str
    repo: str
    issue_number: int
    body: str


@app.post("/post-analysis")
async def post_analysis(req: PostAnalysisRequest):
    """Human-triggered: post the analysis as a comment and add a difficulty label."""
    await post_comment(req.owner, req.repo, req.issue_number, req.body)

    # Pull just the 'Recommended Skill Level' line to avoid matching stray
    # words like 'junior' in the Mentorship Notes. Longest key wins so
    # 'senior+' beats 'senior' and 'mid-level' beats 'mid'.
    import re
    match = re.search(r"recommended skill level.*", req.body, re.IGNORECASE)
    level_line = match.group(0).lower() if match else ""
    for level in sorted(SKILL_LABELS, key=len, reverse=True):
        if level in level_line:
            await add_labels(req.owner, req.repo, req.issue_number, SKILL_LABELS[level])
            break

    return {"status": "posted"}


# =================================================================
# PHASE 6b — Safety: Pre-tool Validation Hook (talk through only)
#
# The SDK lets you intercept tool calls BEFORE they execute.
# This is your last line of defense against prompt injection
# or unexpected agent behaviour.
#
# To enable: add "hooks": {"on_pre_tool_use": validate_tool_args}
# to the create_session() calls above.
# =================================================================

# A function that prevents the agent from reading files outside the repo 
# or sensitive files like .env or credentials.

# async def validate_tool_args(event):
#     """Block dangerous tool arguments before execution."""
#     if event.data.tool_name == "get_file_content":
#         path = event.data.arguments.get("path", "")
#         if ".." in path or path.startswith("/") or path.startswith("~"):
#             print(f"  🛑 BLOCKED: unsafe path — {path}")
#             return {"decision": "reject", "message": "Blocked: unsafe path"}
#         sensitive = [".env", ".git/", "secrets", "credentials", "token"]
#         if any(s in path.lower() for s in sensitive):
#             print(f"  🛑 BLOCKED: sensitive file — {path}")
#             return {"decision": "reject", "message": "Blocked: sensitive file"}
#     return {"decision": "allow"}



# =================================================================
# Helper functions
# =================================================================


def parse_github_url(url: str) -> tuple[str, str, int]:
    """Parse 'https://github.com/owner/repo/issues/123' into parts."""
    parts = url.rstrip("/").replace("https://github.com/", "").split("/")
    if len(parts) >= 4 and parts[2] == "issues":
        return parts[0], parts[1], int(parts[3])
    raise ValueError(f"Invalid GitHub issue URL: {url}")


def _parse_args(raw):
    """Parse tool arguments from the various formats the SDK may return."""
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return {}
    if hasattr(raw, "model_dump"):
        return raw.model_dump()
    return {}



# =================================================================
# CLI Entry Point
# =================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{msg('cli_title')}\n")
        print("  python app_final.py hello                          # Test the SDK (send_and_wait)")
        print("  python app_final.py hello-stream                   # Test with streaming events")
        print("  python app_final.py <github_issue_url>             # CLI analysis")
        print("  python app_final.py <owner> <repo> <issue_number>  # CLI analysis")
        print("  python app_final.py serve                          # Web UI (post via the UI button)")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "hello":
        asyncio.run(hello_world())
    elif cmd == "hello-stream":
        asyncio.run(hello_world_streaming())
    elif cmd == "serve":
        import uvicorn
        # reload=True picks up code changes on save. Pass the import string
        # form ("module:app") rather than the app object so reload can work.
        uvicorn.run("app_final:app", host="0.0.0.0", port=8001, reload=True)
    elif cmd.startswith("https://"):
        owner, repo, num = parse_github_url(cmd)
        asyncio.run(analyse_cli(owner, repo, num))
    elif len(sys.argv) == 4:
        asyncio.run(analyse_cli(sys.argv[1], sys.argv[2], int(sys.argv[3])))
    else:
        print(msg('cli_arg_error'))
        sys.exit(1)
