# Microsoft ブランド スライド (日英 × Light/Dark) 生成スクリプト

このディレクトリは、`presenter-resources/decks/` 配下の **4 種の Microsoft ブランドスライド** (JA/EN × Light/Dark) を再生成するためのソースと手順を含みます。

## ソース

| ファイル | 言語 | テーマ | 出力ファイル |
|---|---|---|---|
| `slides-ja-light.json` | 日本語 | Light (Warm White) | `AI_Genius_Copilot_SDK_Ep3_JA_light.{pptx,pdf}` |
| `slides-ja-dark.json` | 日本語 | Dark (Blue Black) | `AI_Genius_Copilot_SDK_Ep3_JA_dark.{pptx,pdf}` |
| `slides-en-light.json` | 英語 | Light (Warm White) | `AI_Genius_Copilot_SDK_Ep3_EN_light.{pptx,pdf}` |
| `slides-en-dark.json` | 英語 | Dark (Blue Black) | `AI_Genius_Copilot_SDK_Ep3_EN_dark.{pptx,pdf}` |

各 JSON は同じ 5 スライド構成 (title / content 2col / timeline horizontal / content 2x2 / resources) で、`theme` の値と本文の言語だけが異なります。

## 一括生成

```bash
cd presenter-resources/decks/sources
bash build.sh
```

`build.sh` は以下を行います:
1. `microsoft-brand-guidelines` スキル (`~/.copilot/skills/microsoft-brand-guidelines`) の `examples/deck-from-json.js` ランナーを使って 4 種の PPTX を生成
2. LibreOffice headless で 4 種の PDF に変換
3. 結果を 1 階層上 (`presenter-resources/decks/`) に配置

`BRAND_SKILL` 環境変数でスキルパスを上書きできます。

## 個別生成

```bash
# 例: 日本語 Dark 版だけ作り直す
node ~/.copilot/skills/microsoft-brand-guidelines/examples/deck-from-json.js \
  slides-ja-dark.json \
  ../AI_Genius_Copilot_SDK_Ep3_JA_dark.pptx

libreoffice --headless --convert-to pdf --outdir .. \
  ../AI_Genius_Copilot_SDK_Ep3_JA_dark.pptx
```

## 依存

- Node.js 18+ (pptxgenjs)
- LibreOffice (`libreoffice --convert-to pdf`)
- `microsoft-brand-guidelines` スキル (Microsoft Warm White / Blue Black の brand tokens、9 種類のレイアウトを提供)
- 日本語フォント: Yu Gothic UI を優先、Linux では Noto Sans CJK JP に fallback (`fc-cache -f` で有効化)

## レイアウト構成 (5 スライド共通)

| # | layout | variant | 内容 |
|---|---|---|---|
| 1 | `title` | `dark-circles` | タイトル + サブタイトル + クレジット |
| 2 | `content` | `2col` | 2 列比較 (Editor Copilot vs SDK) |
| 3 | `timeline` | `horizontal` | エージェント型ループ (6 stages) |
| 4 | `content` | `2x2` | アーキテクチャ 4 層 |
| 5 | `resources` | (default) | 次のアクション (リンク 4 件) |

## ライブ配信での使い分け

| シーン | 推奨 |
|---|---|
| 日本人向けライブ配信 | `JA_dark` (画面が暗い OBS 配信に映える) |
| 日本人向け資料配布 | `JA_light` (PDF として読みやすい) |
| 英語版アーカイブ作成 | `EN_dark` / `EN_light` (好みで選択) |
| ハイブリッド配信 (二言語並走) | `JA_dark` + `EN_dark` を別モニターに |
