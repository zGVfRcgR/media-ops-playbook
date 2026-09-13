# 運用ワークフロー

## 1. ネタ選定
1. `portfolio-masterplan/docs/daily_logs` を確認する
2. ショート動画向きのテーマを選ぶ
3. リスクの高い題材を分ける
4. 台本化候補を決める

## 2. 台本作成
1. 1本1テーマで作る
2. 冒頭にフックを置く
3. 結論を先に出す
4. 必要ならCTAを付ける

## 3. コンプライアンス確認
1. 税務・法務・金融表現を確認する
2. 断定的な表現を修正する
3. 著作権リスクを確認する
4. 必要なら人間の専門家に回す

## 4. 公開前レビュー
1. 内容の正確性を確認する
2. 表現の強さを調整する
3. 投稿先媒体に合わせて整形する
4. 最終承認を受ける

## 5. 投稿
1. YouTube Shorts 用に整える
2. Instagram Reels 用に整える
3. タイトルと説明文を整える
4. 投稿する

## 6. データ収集（Python 実行）

グロースアナリストと収益化アドバイザーは、分析の前に Python スクリプトで YouTube のデータを取得する。

### 手順
1. 初回のみ依存パッケージをインストールする
   ```bash
   pip install -r python/requirements.txt
   ```
2. プロジェクトルートで `.env.example` を `.env` にコピーし、値を設定する
   ```bash
   cp .env.example .env
   ```
   設定内容:
   ```
   YOUTUBE_API_KEY=<Google Cloud で発行した API キー>
   YOUTUBE_CHANNEL_ID=<分析対象のチャンネル ID>
   MAX_COMMENTS_PER_VIDEO=100
   ```
3. スクリプトを実行する
   ```bash
   python python/youtube_collector.py
   ```
4. `data/` フォルダに以下のファイルが生成される
   - `channel_info.json` — チャンネルメタデータ
   - `videos.json` / `videos.csv` — 全動画の詳細・統計
   - `comments.json` / `comments.csv` — トップレベルコメント

### 取得フィールドの定義
`youtube/fields.md` を参照する。

### 注意事項
- YouTube Data API v3 の無料クォータは 1 日 10,000 ユニットです。
- クォータが不足する場合は取得動画数を分割して実行してください。
- API キーをリポジトリにコミットしてはいけません。`.env` ファイルは `.gitignore` で除外してください。

---

## 7. 分析（グロースアナリスト・収益化アドバイザー）

1. `data/videos.csv` を開き、以下の観点で分析する
   - `view_count` の高い動画のタイトル・タグ・曜日を確認する
   - `is_shorts` フラグでショート動画と通常動画を分けて比較する
   - `title_length` と `view_count` の相関を確認する
   - 投稿 `weekday` と視聴数の傾向を把握する
2. `data/comments.csv` を開き、以下を確認する
   - `like_count` の高いコメントからニーズを抽出する
   - キーワード頻度で視聴者の関心を整理する
3. 分析結果を `analytics/kpi_template.md` の記録欄に記入する
4. 改善案を Copilot に提示して次回の台本・タイトル案を生成する

---

## 8. 改善
1. 良かった点を残す
2. 弱かった点を1つだけ改善する
3. 次の動画に反映する

## 9. コメント対応
1. コメントを分類する
2. 返信案を作る
3. 危険なものは人間に回す
4. 落ち着いた応対を優先する
