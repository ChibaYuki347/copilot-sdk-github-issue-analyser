# 日本語スライド生成スクリプト

このディレクトリには、`AI_Genius_Copilot_SDK_Ep3_JA.pptx` / `.pdf` を再生成するための入力 JSON と手順が入っています。

## ソース

- `slides.json` — Microsoft ブランドガイドラインの pptxgenjs レイアウト用 JSON 仕様
  - 5 スライド構成: title / content(2col) / timeline(horizontal) / content(2x2) / resources
  - `step-by-step/slides.ja.md` の内容を JSON 化したもの

## 生成方法

```bash
# 1. pptxgenjs ランナーで PPTX 生成 (Microsoft ブランドガイドライン)
node ~/.copilot/skills/microsoft-brand-guidelines/examples/deck-from-json.js \
  slides.json \
  ../AI_Genius_Copilot_SDK_Ep3_JA.pptx

# 2. PDF に変換
libreoffice --headless --convert-to pdf --outdir .. ../AI_Genius_Copilot_SDK_Ep3_JA.pptx
```

## 使用したスキル

- [`microsoft-brand-guidelines`](https://github.com/ChibaYuki347/microsoft-brand-guidelines) skill
  - `layouts/pptxgenjs/` の 9 レイアウトを使用
  - `tokens/light.json` (Microsoft Warm White ベース)
- LibreOffice (PDF 変換)

## 日本語フォント

- ヘッダー: Yu Gothic UI (Windows / macOS)、Linux では Noto Sans CJK JP に fallback
- 本文: Yu Gothic UI / Noto Sans CJK JP

CJK フォントがインストールされていない環境では `fc-cache -f` で Noto CJK を有効化してください。
