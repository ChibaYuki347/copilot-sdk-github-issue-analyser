# 日本語版 (`ja` ブランチ) の運用ガイド

このリポジトリは Renee Noble さんが管理する [`reneenoble/copilot-sdk-github-issue-analyser`](https://github.com/reneenoble/copilot-sdk-github-issue-analyser) のフォークです。日本語向け教材は `ja` ブランチで管理しており、`main` は upstream に追随します。本ドキュメントはその運用方法を説明します。

---

## 1. ブランチ構成

```
upstream (reneenoble/copilot-sdk-github-issue-analyser)
└── main
        │
        ▼ (定期同期)
ChibaYuki347/copilot-sdk-github-issue-analyser (fork)
├── main   ← upstream/main と常に同一に保つ (日本語ファイルを足さない)
└── ja     ← 日本語版教材を追加した派生ブランチ (本番デモはここから配信)
```

**設計原則**:

- 英語のオリジナルファイルは原則として変更しない (sync 時の競合を最小化)。
- 日本語版は `README.ja.md`, `*.ja.md`, `*_JA.pdf` のように**サフィックス命名で並存**させる。
- 唯一の例外として `README.md` の冒頭に「日本語版はこちら」リンクとクレジットの数行を追加する (`ja` ブランチに含めるが、upstream にも PR してマージしてもらうことを目指す)。

---

## 2. リモート設定 (初回のみ)

```bash
git clone https://github.com/ChibaYuki347/copilot-sdk-github-issue-analyser.git
cd copilot-sdk-github-issue-analyser
git remote add upstream https://github.com/reneenoble/copilot-sdk-github-issue-analyser.git
git remote -v
# origin   = ChibaYuki347/... (fetch/push)
# upstream = reneenoble/...   (fetch/push)
```

ローカル `main` を upstream 追跡に切り替え:

```bash
git checkout main
git branch --set-upstream-to=upstream/main main
```

---

## 3. upstream → main の同期 (定期作業)

```bash
git checkout main
git fetch upstream --no-tags
git merge --ff-only upstream/main   # 早送りマージのみ許可
git push origin main                # 自分のフォークにも反映
```

`fast-forward` できない (= 自分が main に直接コミットしてしまった) 場合は、その変更を ja ブランチに移してから main をリセットしてください。

---

## 4. main → ja の取り込み (upstream が更新された後)

```bash
git checkout ja
git merge main
# 衝突した場合は README.md (冒頭バナー追記箇所) を中心に解決
git push origin ja
```

衝突しやすい箇所:

| ファイル | 想定衝突 | 解決方針 |
|---|---|---|
| `README.md` | 冒頭の Language switch バナー | `ja` 側を採用しつつ、`main` から来た本文の更新を取り込む |
| `app.py` | 大きな機能追加が upstream に入った場合 | `ja` ブランチ側のロジック (LANG 切替) を保ったまま、新機能を取り込む |
| `presenter-resources/` | プレゼンター用ファイルの更新 | 基本的に `main` を採用。日本語版独自ファイル (`*_JA.pdf` 等) はそのまま |

---

## 5. ja ブランチで追加するファイルの命名規則

| パターン | 例 |
|---|---|
| `<name>.ja.md` | `README.ja.md`, `AGENTS.ja.md`, `docs/RAI.ja.md`, `step-by-step/build-guide.ja.md` |
| `<name>_JA.pdf` | `presenter-resources/AI_Genius_Copilot_SDK_Ep3_JA.pdf` |
| 新規日本語専用ファイル | `step-by-step/glossary.ja.md`, `step-by-step/system-prompt.ja.md`, `docs/SYNCING-UPSTREAM.ja.md` (本ファイル) |

---

## 6. upstream に貢献する場合 (任意)

日本語化作業の中で「英語版にも反映する価値がある」改善 (例: `pre-stream-check.sh` のバグ修正、誤字修正) を見つけたら、以下の手順で upstream に PR を投げます:

```bash
git checkout main
git pull upstream main
git checkout -b fix/<topic>
# 変更を作成
git push origin fix/<topic>
gh pr create --repo reneenoble/copilot-sdk-github-issue-analyser --base main
```

日本語版固有の追加 (`*.ja.md` 等) は upstream にマージしてもらう必要はありません (ja ブランチで完結)。

---

## 7. リリース運用 (ライブ配信前)

ライブ配信の数日前に以下を行います:

```bash
# 1. 最新の upstream を取り込む
git checkout main
git fetch upstream && git merge --ff-only upstream/main
git push origin main

# 2. main の変更を ja に取り込む
git checkout ja
git merge main
git push origin ja

# 3. pre-stream-check を ja ブランチで実行
bash presenter-resources/pre-stream-check.sh

# 4. 日本語動作の確認
LANG=ja python app.py hello
LANG=ja python app.py serve   # ブラウザで http://localhost:8000

# 5. デモ用 issue (英語版 + 日本語版) を最終チェック
python app.py <英語 issue の URL>
LANG=ja python app.py <日本語 issue の URL>
```

---

## 8. 配信後 (任意)

配信が成功したら、ja ブランチを `ja-stable-YYYY-MM-DD` のようなタグとして固定し、視聴者が当時の構成を再現できるようにすると親切です。

```bash
git checkout ja
git tag -a ja-stable-2026-05-20 -m "Livestream snapshot for Japanese audience demo"
git push origin ja-stable-2026-05-20
```
