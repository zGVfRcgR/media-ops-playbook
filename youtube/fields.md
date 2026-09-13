# YouTube Data API 取得フィールド定義

グロースアナリストと収益化アドバイザーが分析に使うフィールドを定義します。  
Python コレクタースクリプト（`python/youtube_collector.py`）がこの定義に基づいてデータを取得します。

---

## 1. チャンネルメタデータ（channels.list）

| フィールド | API パス | 用途 |
|---|---|---|
| チャンネルID | `id` | 一意識別子 |
| チャンネル名 | `snippet.title` | 表示名 |
| 説明文 | `snippet.description` | チャンネルコンセプト確認 |
| 公開日 | `snippet.publishedAt` | 運用年数の計算 |
| 国設定 | `snippet.country` | ターゲット地域確認 |
| キーワード | `brandingSettings.channel.keywords` | SEO分析 |
| 登録者数 | `statistics.subscriberCount` | 規模感の把握 |
| 総再生回数 | `statistics.viewCount` | チャンネル全体パフォーマンス |
| 総動画数 | `statistics.videoCount` | 投稿量の把握 |
| アップロード用プレイリストID | `contentDetails.relatedPlaylists.uploads` | 動画一覧取得に使用 |

---

## 2. 動画メタデータ（videos.list – snippet）

| フィールド | API パス | 用途 |
|---|---|---|
| 動画ID | `id` | 一意識別子 |
| タイトル | `snippet.title` | フック分析 |
| 説明文 | `snippet.description` | CTA・キーワード確認 |
| 公開日時 | `snippet.publishedAt` | 投稿頻度分析 |
| サムネイルURL | `snippet.thumbnails.high.url` | サムネイル比較 |
| タグ | `snippet.tags` | SEO・テーマ分析 |
| カテゴリID | `snippet.categoryId` | ジャンル分類 |
| ライブ配信区分 | `snippet.liveBroadcastContent` | 通常動画／ライブ区別 |
| 動画時間 | `contentDetails.duration` | ショート動画判定（60秒以内） |
| キャプション有無 | `contentDetails.caption` | アクセシビリティ確認 |

---

## 3. 動画パフォーマンス統計（videos.list – statistics）

| フィールド | API パス | 用途 |
|---|---|---|
| 再生数 | `statistics.viewCount` | 人気度の把握 |
| 高評価数 | `statistics.likeCount` | 共感度の把握 |
| コメント数 | `statistics.commentCount` | エンゲージメント測定 |
| お気に入り数 | `statistics.favoriteCount` | 保存意向の把握 |
| 取得日時（スクリプト付与） | `fetched_at` | 時系列比較用 |

---

## 4. コメント（commentThreads.list）

| フィールド | API パス | 用途 |
|---|---|---|
| コメントスレッドID | `id` | 一意識別子 |
| コメント本文 | `snippet.topLevelComment.snippet.textOriginal` | テキスト分析 |
| 投稿日時 | `snippet.topLevelComment.snippet.publishedAt` | 時系列確認 |
| いいね数 | `snippet.topLevelComment.snippet.likeCount` | 共感コメント抽出 |
| 返信数 | `snippet.totalReplyCount` | 議論の深さ確認 |
| 投稿者名 | `snippet.topLevelComment.snippet.authorDisplayName` | コミュニティ分析 |

---

## 5. 分析補助フィールド（スクリプト側で付与）

| フィールド | 付与方法 | 用途 |
|---|---|---|
| ショート動画フラグ | duration ≤ 60秒で判定 | ショート専用分析 |
| 投稿曜日 | `publishedAt` から計算 | 投稿タイミング分析 |
| タイトル文字数 | `title` の文字数 | フック最適化 |
| 説明文文字数 | `description` の文字数 | CTA設計分析 |
| タグ数 | `tags` のリスト長 | SEO戦略確認 |

---

## 参考：今後追加を検討するAPI

- **YouTube Analytics API**: 視聴維持率・トラフィックソース・視聴者属性など詳細データ（OAuth 2.0 必須）
- **YouTube Reporting API**: 大量データの定期バルク取得

> **注意**: YouTube Data API v3 の無料クォータは1日10,000ユニットです。大量取得時はクォータ消費に注意してください。
