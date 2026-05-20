# 用語集 (日本語版ワークショップ統一用)

> このファイルは日本語版教材 (`*.ja.md` / 日本語 PDF / Web UI の日本語表示) で使う用語を統一するための基準です。翻訳・口頭発表の前にここの語を必ず参照してください。

## 1. 翻訳方針

- **直訳寄り**: 原文 (英語) のニュアンスを保つことを優先する。
- **GitHub の UI 用語はそのまま英語表記** (例: Issue, Pull request, Codespaces)。日本語にすると GitHub 画面と一致せず混乱の元になる。
- **コードのシンボル名 (関数・変数・クラス名) は翻訳しない**。これらは `app.py` 内で英語のまま残す。
- 説明文中で英語の固有名詞を使うときは初出時に括弧で日本語訳を添える: 例 `Session (セッション)`。

## 2. SDK / 技術用語

| 英語 | 日本語 (推奨) | 備考 |
|---|---|---|
| Copilot SDK | Copilot SDK | そのまま (公式名称) |
| Client | クライアント | `CopilotClient` はコード上は英語のまま |
| Session | セッション | |
| Tool / Tools | ツール | |
| Tool call | ツール呼び出し | |
| Tool definition | ツール定義 | `@define_tool` デコレータの説明用 |
| Agent | エージェント | |
| Agentic | エージェント型 | "エージェント的" よりこちらを推奨 |
| Streaming | ストリーミング | |
| Event | イベント | |
| Event type | イベント種別 | |
| `assistant.message` | (英語のまま) | コードに現れるリテラルなので翻訳しない |
| `tool.call` | (英語のまま) | 同上 |
| `session.idle` | (英語のまま) | 同上 |
| System prompt | システムプロンプト | |
| Prompt | プロンプト | |
| Permission handler | パーミッションハンドラ | |
| `send_and_wait` | (英語のまま) | API 名 |
| Multi-turn tool loop | マルチターンのツールループ | |

## 3. GitHub 用語

| 英語 | 日本語 (推奨) | 備考 |
|---|---|---|
| Issue | Issue | 英語のまま (GitHub UI 一致) |
| Pull request / PR | Pull request | 英語のまま |
| Repository / Repo | リポジトリ | |
| Branch | ブランチ | |
| Codespaces | Codespaces | 英語のまま |
| Dev Container | Dev Container | 英語のまま |
| Personal access token (PAT) | パーソナルアクセストークン (PAT) | |
| Fine-grained token | きめ細かいトークン (Fine-grained token) | GitHub 画面の用語と併記 |
| Token | トークン | |
| Scope | スコープ | |
| REST API | REST API | |
| Webhook | Webhook | 英語のまま |
| Label | ラベル | |
| Comment | コメント | |
| Triage | トリアージ | 初出時に「(課題の選別)」と注釈 |
| Code search | コード検索 | |
| Directory listing | ディレクトリ一覧 | |

## 4. 開発者スキルレベル (重要・誤解防止)

> ⚠️ ライブ配信で読み上げる際、必ず一度「**これは年次の話ではなく、コードベースへの習熟度です**」と明示すること。

| 英語 | 日本語 (推奨) | 補足 |
|---|---|---|
| Junior | ジュニア | 「初級」と訳すと年功色が出るためカタカナ |
| Mid-level | ミドル | 「中級」より「ミドル」推奨 (RAI 注に従う) |
| Senior | シニア | |
| Senior+ / Team effort | シニア+ / チーム対応 | |
| Skill level | スキルレベル | |
| Codebase familiarity | コードベースへの習熟度 | RAI 注のキーフレーズ |
| Mentorship notes | メンタリングのヒント | |
| Confidence (High / Medium / Low) | 確信度 (高 / 中 / 低) | |

## 5. Responsible AI 関連

| 英語 | 日本語 (推奨) | 備考 |
|---|---|---|
| Responsible AI (RAI) | 責任ある AI (RAI) | 略称 RAI も併用可 |
| Bias | バイアス | |
| Language bias | 言語バイアス | **Demo 2 (日本語 issue) で必ず触れる** |
| Issue quality bias | Issue 品質バイアス | |
| Repository bias | リポジトリバイアス | |
| Transparency | 透明性 | |
| Human oversight | 人間による監督 | |
| Recommendation / not decision | 推奨であり、決定ではない | 重要フレーズ |

## 6. ライブ配信構成の用語

| 英語 | 日本語 (推奨) | 備考 |
|---|---|---|
| Livestream | ライブ配信 | "ライブストリーム" でも可 |
| Phase | フェーズ | Phase 1 → フェーズ 1 |
| Talking points | トーキングポイント (要点) | 直訳でも可 |
| Demo | デモ | |
| Code highlight | コードのハイライト | |
| Pre-stream check | 配信前チェック | `pre-stream-check.sh` ファイル名は英語のまま |
| Wrap-up | まとめ | |
| Q&A | Q&A | 英語のまま |
| Web UI / Web app | Web UI / Web アプリ | |
| Frontend | フロントエンド | |
| Server-Sent Events (SSE) | Server-Sent Events (SSE) | 英語のまま |

## 7. ファイル命名規約

| パターン | 用途 |
|---|---|
| `<name>.md` | 英語版 (upstream と同一・原則手を入れない) |
| `<name>.ja.md` | 日本語版 (新規追加) |
| `glossary.ja.md` | 本ファイル |
| `presenter-resources/AI_Genius_Copilot_SDK_Ep3_EN.pdf` | 英語スライド PDF (upstream の既存ファイル) |

## 8. クレジット表記の標準フレーズ

すべての `*.ja.md` の冒頭付近に、以下のいずれかの形で含める:

```markdown
> 🌏 **Language / 言語**: [English (original)](README.md) · [日本語版](README.ja.md)
>
> Original workshop by **Renee Noble** ([reneenoble/copilot-sdk-github-issue-analyser](https://github.com/reneenoble/copilot-sdk-github-issue-analyser)).
> 日本語版作成: **@ChibaYuki347**. MIT License.
```

短縮形 (脚注向け):

```markdown
*原著: Renee Noble (reneenoble/copilot-sdk-github-issue-analyser) / 日本語版: @ChibaYuki347*
```

## 9. 文体ルール

- 基本は「**ですます調**」(丁寧体) でライブ配信での読み上げに自然なトーン。
- コードのコメント (`# ...`) は短い体言止め or 簡潔な「ですます」のどちらでも可。冗長にしないこと。
- 命令形 (例: "Click X") は「X をクリックします」(指示) または「X をクリックしてください」(視聴者への呼びかけ) を文脈で使い分け。
- 絵文字は原文と同じ箇所のみに留め、勝手に増やさない。
