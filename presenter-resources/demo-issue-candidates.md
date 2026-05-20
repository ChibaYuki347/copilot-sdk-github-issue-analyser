# 日本語 Issue デモ候補

> ライブ配信用に選定した日本語 GitHub Issue の候補です。Demo 2 (RAI Language bias) セクションで使用します。  
> 最終調査日: 2026-05-19  
> 補足: 依頼の「2025-11 時点」条件に合わせ、**2025-11 までに作成済み** かつ **2026-05-19 現在も open** の issue に限定しました。

- **リポジトリ活動確認**: `VOICEVOX/voicevox` は 2026-05-18 push、`VOICEVOX/voicevox_engine` は 2026-05-13 push（いずれも `gh repo view` で確認）

## ⚙️ 練習・自前デモ用フォールバック

VOICEVOX への投稿は本番限定とし、**配信前のリハーサルや、自分の repo を analysis 結果で汚したくないケース** では Renee さん公式の練習用リポジトリを使えます:

- **`reneenoble/demo_project_with_issues`** — https://github.com/reneenoble/demo_project_with_issues
  - fork 可。基本的な Python プロジェクトに「いろいろな難易度の問題」が仕込まれています
  - リポ内のスクリプトで **任意難易度の issue を一括生成** できます (タグなしで何度でも spam push して大丈夫)
  - 英語の issue が中心なので、本配信の Demo 2 (日本語 issue) には使えません。**英語ベースのリハーサル / 練習用** と割り切るのが良いです
  - Renee さんからのメッセージ (2026-05-20 dry run フィードバック): 「自分の repo を spam したくないなら、私のデモ用リポを fork してください。難易度別 issue を生成するスクリプトも入っています」

## 本命 (Primary)


### 1. [VOICEVOX/voicevox] — Linux版0.24.0以降でプロジェクトファイルが保存されない
- **URL**: https://github.com/VOICEVOX/voicevox/issues/2723
- **言語比率**: タイトル日本語 / body 日本語（ログ引用あり） / comments 日本語
- **想定スキルレベル**: Mid-level（Electron の保存ダイアログと Linux/KDE 環境差分の切り分けが必要）
- **複雑度の見立て**: 保存ダイアログ周り・Electron bridge・Linux 向け分岐・再現確認をまたぐバグ修正になりそう
- **デモ向け魅力**: issue テンプレが整っていて再現手順とログが明確。コメントで upstream/Electron 由来の示唆もあり、Copilot SDK の解析デモで「切り分け」を見せやすい

## バックアップ (Backup)

### 2. [VOICEVOX/voicevox_engine] — pyproject.tomlのバージョン管理問題をなんとかしたい
- **URL**: https://github.com/VOICEVOX/voicevox_engine/issues/1797
- **言語比率**: タイトル日本語（ファイル名含む） / body 日本語 / comments 日本語
- **想定スキルレベル**: Mid-level（パッケージ metadata・Python 側 version 定義・build workflow の整合が必要）
- **複雑度の見立て**: `pyproject.toml`・`voicevox_engine/__init__.py`・GitHub Actions を 2〜3 箇所またいで直すタイプ
- **デモ向け魅力**: 問題箇所が本文に具体的に書かれており、解析結果の再現性が高い。Mid-level 判定に寄せやすい

### 3. [VOICEVOX/voicevox] — AppImage配布の形式を、分割7zから分割tar.gzか分割無圧縮に変更する
- **URL**: https://github.com/VOICEVOX/voicevox/issues/2845
- **言語比率**: タイトル日本語（技術用語含む） / body 日本語 / comments 日本語
- **想定スキルレベル**: Mid-level（Linux 配布形式変更と installer / release 導線の整合確認が必要）
- **複雑度の見立て**: `installer_linux.sh`・配布アセット生成・案内文書の更新が必要そうで、変更範囲は中程度
- **デモ向け魅力**: Pros / Cons とコメント議論が充実しており、単純修正ではないが Team effort までは行かない、ちょうど良い中難度

### 4. [VOICEVOX/voicevox] — スナップショットが意図せずアップデートされてしまう問題
- **URL**: https://github.com/VOICEVOX/voicevox/issues/2731
- **言語比率**: タイトル日本語 / body 日本語 / comments なし
- **想定スキルレベル**: Mid-level（snapshot 更新手順・テスト基盤・差分発生条件の理解が必要）
- **複雑度の見立て**: snapshot 更新スクリプト、README 上の運用手順、テスト設定の 2〜3 箇所を追う調査系バグ
- **デモ向け魅力**: 本文が短くても論点が明確で、Copilot SDK が不足情報を補いながら「何を見に行くべきか」を出すデモに向く

## その他参考 (Reference)

### 5. [VOICEVOX/voicevox] — 音声キャラクター選択の利便性向上
- **URL**: https://github.com/VOICEVOX/voicevox/issues/2695
- **言語比率**: タイトル日本語 / body 日本語 / comments 日本語
- **想定スキルレベル**: Mid-level 寄り（UI 改善だが、既存の並び替え・ピン留め相当の挙動との整合が必要）
- **複雑度の見立て**: キャラクター選択 UI、最近使った一覧の状態保持、既存順序ロジックの整理が必要そう
- **デモ向け魅力**: 一般視聴者にも直感的に伝わる内容で、日本語 issue として読みやすい。少し軽めなので予備候補向き

## 不採用候補とその理由
- `kintone-labs/kintone-ui-component`: 直近 1 年以内に **created / updated とも条件を満たす** open な日本語本文 issue を確認できず
- `yamadashy/repomix#352`, `#379`: 本文が中国語主体で、日本語 issue 候補としては不適
- `denoland/deno`, `lvgl/lvgl`: open issue を広く確認した範囲で、日本語本文の moderate 候補を見つけられず
- `gatsbyjs/gatsby-i18n`: `gh repo view` でリポジトリを解決できず
- `VOICEVOX/voicevox#2733`: 日本語 issue としては優秀だが、UI・データ構造・編集体験の議論が広く、Mid-level より重め
- `VOICEVOX/voicevox#2677`: 要望が広すぎて実装粒度が曖昧で、解析結果が散りやすい
- `VOICEVOX/voicevox_engine#1784`: `初心者歓迎タスク` で、ライブ配信デモの moderate 候補としてはやや軽い
