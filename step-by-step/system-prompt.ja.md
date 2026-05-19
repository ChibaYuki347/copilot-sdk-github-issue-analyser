> 🌏 これは `app.py` を `LANG=ja` モードで動かすときに使う日本語文字列の参考資料です。実装担当者 (呼び出し元) がこのファイルを参照しながら `app.py` をパラメータ化します。
>
> 日本語版作成: **@ChibaYuki347**. Original by Renee Noble. MIT License.

# app.py 日本語文字列リファレンス

## 1. SYSTEM_PROMPT

### SYSTEM_PROMPT
**英語原文:**
```text
You are a senior engineering manager triaging GitHub issues.

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
Include what a less experienced developer would need to learn to tackle this issue.
```

**日本語訳 (LANG=ja で使用):**
```text
あなたは GitHub Issue をトリアージするシニアエンジニアリングマネージャーです。

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
```

## 2. CLI 向け文言

| 場面 | 英語 (原文) | 日本語 (LANG=ja) |
|---|---|---|
| 解析開始時 | 🔍 Analysing issue #{issue_number} in {owner}/{repo}... | 🔍 {owner}/{repo} の Issue #{issue_number} を解析しています... |
| ツール実行開始時 | 🔧 {tool}... | 🔧 {tool} を実行しています... |
| コメント投稿完了時 | 💬 Comment posted to {owner}/{repo}#{issue_number} | 💬 {owner}/{repo}#{issue_number} にコメントを投稿しました |
| ラベル追加完了時 | 🏷️  Labels added: {labels} | 🏷️  ラベルを追加しました: {labels} |
| CLI ヘルプ見出し | 🐛 GitHub Issue Complexity Analyser — Livestream Build | 🐛 GitHub Issue Complexity Analyser — ライブ配信ビルド |
| SDK テストの使い方 | `python stream_api.py hello` # Test the SDK (send_and_wait) | `python stream_api.py hello` # SDK をテストします (send_and_wait) |
| ストリーミングテストの使い方 | `python stream_api.py hello-stream` # Test with streaming events | `python stream_api.py hello-stream` # ストリーミングイベントでテストします |
| URL 指定の解析方法 | `python stream_api.py <github_issue_url>` # CLI analysis | `python stream_api.py <github_issue_url>` # CLI 解析 |
| owner / repo / 番号指定の解析方法 | `python stream_api.py <owner> <repo> <issue_number>` # CLI analysis | `python stream_api.py <owner> <repo> <issue_number>` # CLI 解析 |
| Web UI の起動方法 | `python stream_api.py serve` # Web UI | `python stream_api.py serve` # Web UI |
| 解析して Issue に投稿する方法 | `python stream_api.py post <github_issue_url>` # Analyse + post to issue | `python stream_api.py post <github_issue_url>` # 解析して Issue に投稿します |
| URL 解析エラー | Invalid GitHub issue URL: {url} | GitHub Issue URL が不正です: {url} |
| 引数エラー | Error: Invalid arguments. Run without args for usage. | エラー: 引数が不正です。使い方を表示するには引数なしで実行してください。 |

## 3. FastAPI / SSE / ツール返却文言

> 注: 現在の `app.py` には `HTTPException` による固定文言はありません。ここでは、`app.py` 内に明示的に書かれている status / error 文字列を抜き出しています。

| 種別 | 英語 (原文) | 日本語 (LANG=ja) | 備考 |
|---|---|---|---|
| `/health` の status | `healthy` | `正常` | `{"status": "healthy"}` |
| SSE 完了 status | `complete` | `完了` | `event: done` の data 内 |
| `/post-analysis` の status | `posted` | `投稿済み` | `{"status": "posted"}` |
| Issue 本文なし時の既定値 | `No description` | `説明はありません` | `get_github_issue` |
| Issue 取得エラー | `Error fetching issue: {e}` | `Issue の取得中にエラーが発生しました: {e}` | `get_github_issue` |
| 単一ファイルの表示 | `File: {path}` | `ファイル: {path}` | `get_repo_structure` |
| コード検索ヒットなし | `No matching code found` | `一致するコードは見つかりませんでした` | `search_code_in_repo` |
| 汎用エラー | `Error: {e}` | `エラー: {e}` | `get_repo_structure` / `search_code_in_repo` / `get_file_content` |
| デコード失敗 | `Unable to decode` | `デコードできません` | `get_file_content` |

### 補足

- SSE のイベント名である `message` / `tool_call` / `done` は、プロトコル識別子なので翻訳しません。
- SSE の JSON キーである `content` / `name` / `args` / `status` も、実装互換性のため英語のまま保持します。
